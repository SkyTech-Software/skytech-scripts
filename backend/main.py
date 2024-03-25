from fastapi import FastAPI, Depends
from backend.security.auth import validate_api_key
from backend.api_v1.api import api_router
from backend.core.config import settings
from sqlmodel import SQLModel
from backend.db.models import engine

app = FastAPI(
    title=settings.project_name,
    openapi_url="/scripts/api/openapi.json",
    docs_url="/scripts/api/docs" if settings.app_env == "LOCAL" else None,
    dependencies=[Depends(validate_api_key)],
)

SQLModel.metadata.create_all(engine)

app.include_router(api_router, prefix="/scripts/api/v1")
