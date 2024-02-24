from fastapi import HTTPException, Header
from backend.core.config import settings


def validate_api_key(api_key: str = Header(...)) -> str:
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Not authenticated.")
    return api_key
