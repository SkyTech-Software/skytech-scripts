from pydantic_settings import BaseSettings
from os import environ


class Settings(BaseSettings):
    app_env: str = environ["APP_ENV"]
    api_v1_str: str = "/scripts/api/v1"
    project_name: str = "skytech-scripts"
    docs_url: str = "/api/docs"
    api_key: str = environ["API_KEY"]
    smtp_server: str = environ["SMTP_SERVER"]
    smtp_port: str = environ["SMTP_PORT"]
    mailer_username: str = environ["MAILER_USERNAME"]
    mailer_password: str = environ["MAILER_PASSWORD"]
    celery_broker_url: str = environ["CELERY_BROKER_URL"]
    celery_result_backend_url: str = environ["CELERY_RESULT_BACKEND_URL"]


settings = Settings()
