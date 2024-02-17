from fastapi import APIRouter

from backend.api_v1.endpoints import imei_checker

api_router = APIRouter()
api_router.include_router(imei_checker.router, tags=["imei-checker"], prefix="/imei-checker")
