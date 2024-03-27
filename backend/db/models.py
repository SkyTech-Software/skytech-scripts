from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlmodel import create_engine
from backend.core.config import settings


class SkyTechScriptsLogs(SQLModel, table=True):  # type: ignore
    __tablename__ = "skytech_scripts_logs"
    id: int = Field(primary_key=True, index=True)
    task_id: str
    task_name: str
    task_response: str
    task_execution_time: float = Field(nullable=True)
    task_error_message: str = Field(nullable=True)
    log_time: datetime


engine = create_engine(settings.pg_database_url)
