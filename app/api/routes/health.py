from fastapi import APIRouter, Response


router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "Running"}


@router.get("/")
def root():
    return {
        "service": "Api-service",
        "status": "Running",
        "docs": "/docs",
    }


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)
