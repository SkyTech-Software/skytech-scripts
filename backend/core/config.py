from pydantic_settings import BaseSettings
from os import environ


class Settings(BaseSettings):
    api_v1_str: str = "/ls/api/v1"
    project_name: str = "license-server"
    docs_url: str = "/api/docs"
    api_key: str = environ.get("API_KEY")
    sqlalchemy_database_url: str = environ.get("SQLALCHEMY_DATABASE_URL")


settings = Settings()
