from sqlmodel import create_engine
from backend.core.config import settings
from sqlmodel import Session
from typing import Generator

engine = create_engine(settings.sqlalchemy_database_url)


def get_db() -> Generator:
    with Session(engine) as session:
        yield session
