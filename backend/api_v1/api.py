from fastapi import APIRouter

from backend.api_v1.endpoints import license

api_router = APIRouter()
api_router.include_router(license.router, tags=["license"], prefix="/license")
