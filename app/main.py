import secrets
import time
from collections import defaultdict

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .ai_service import get_ai_response
from .crud import save_chat
from .database import Base, SessionLocal, engine
from .models import Partner
from .schemas import ChatRequest, PartnerCreate, PartnerOut

app = FastAPI(title="Api-service")


@app.on_event("startup")
def startup():
    """Create DB tables on startup (non-blocking)."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        pass  # Tables created on first use if DB was unavailable


# Dependency: database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "Running"}


@app.get("/")
def root():
    return {
        "service": "Api-service",
        "status": "Running",
        "docs": "/docs",
    }


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


@app.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    ai_reply = get_ai_response(request.message)
    save_chat(db, request.message, ai_reply)
    return {"response": ai_reply}


# -----------------------------
# Partner management (API keys)
# -----------------------------


@app.post("/partners", response_model=PartnerOut)
def create_partner(partner_in: PartnerCreate, db: Session = Depends(get_db)):
    """
    Simple endpoint to create partners for testing.
    In a real system this would be protected (admin-only).
    """

    api_key = secrets.token_hex(16)

    partner = Partner(
        name=partner_in.name,
        rate_limit_per_minute=partner_in.rate_limit_per_minute,
        api_key=api_key,
    )

    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner


@app.get("/partners", response_model=list[PartnerOut])
def list_partners(db: Session = Depends(get_db)):
    """
    List all partners (for debugging/demo).
    """

    result = db.execute(select(Partner))
    partners = result.scalars().all()
    return partners


# -----------------------------
# Auth + rate limiting
# -----------------------------

JSONPLACEHOLDER_BASE_URL = "https://jsonplaceholder.typicode.com"

# in-memory structure: {partner_id: {minute_ts: count}}
rate_limit_state: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))


def get_current_partner(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> Partner:
    """
    Resolve the calling partner from X-API-Key header.
    """

    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )

    result = db.execute(select(Partner).where(Partner.api_key == x_api_key))
    partner = result.scalars().first()

    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return partner


def check_rate_limit(partner: Partner) -> None:
    """
    Very simple per-partner, per-minute rate limiting stored in memory.
    Good enough for a proof-of-concept.
    """

    current_minute = int(time.time() // 60)
    used = rate_limit_state[partner.id][current_minute]

    if used >= partner.rate_limit_per_minute:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )

    rate_limit_state[partner.id][current_minute] += 1


# -----------------------------
# JSONPlaceholder proxy routes
# -----------------------------


@app.get("/proxy/users")
def proxy_users(partner: Partner = Depends(get_current_partner)):
    """
    Proxy to JSONPlaceholder /users.
    Protected by partner auth + rate limiting.
    """

    check_rate_limit(partner)

    with httpx.Client() as client:
        resp = client.get(f"{JSONPLACEHOLDER_BASE_URL}/users", timeout=10)

    if resp.status_code >= 400:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Upstream error: {resp.text}",
        )

    return resp.json()


@app.get("/proxy/users/{user_id}")
def proxy_user_detail(user_id: int, partner: Partner = Depends(get_current_partner)):
    """
    Proxy to JSONPlaceholder /users/{id}.
    """

    check_rate_limit(partner)

    with httpx.Client() as client:
        resp = client.get(
            f"{JSONPLACEHOLDER_BASE_URL}/users/{user_id}",
            timeout=10,
        )

    if resp.status_code >= 400:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Upstream error: {resp.text}",
        )

    return resp.json()
