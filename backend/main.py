from fastapi import FastAPI, Depends
from backend.security.auth import validate_api_key
from backend.api_v1.api import api_router
from backend.core.config import settings

app = FastAPI(
    title=settings.project_name,
    openapi_url=f"/ls/api/openapi.json",
    docs_url="/ls/api/docs",
    dependencies=[Depends(validate_api_key)],
)

app.include_router(api_router, prefix="/ls/api/v1")
