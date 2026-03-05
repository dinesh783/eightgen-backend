import hashlib

from app.core.config import settings


def hash_api_key(raw_api_key: str) -> str:
    payload = f"{settings.api_key_pepper}:{raw_api_key}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
