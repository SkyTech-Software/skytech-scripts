from pydantic_settings import BaseSettings
from os import environ


class Settings(BaseSettings):
    api_v1_str: str = "/scripts/api/v1"
    project_name: str = "skytech-scripts"
    docs_url: str = "/api/docs"
    api_key: str = environ.get("API_KEY")
    smtp_server: str = environ.get("SMTP_SERVER")
    smtp_port: int = environ.get("SMTP_PORT")
    mailer_username: str  = environ.get("MAILER_USERNAME")
    mailer_password: str = environ.get("MAILER_PASSWORD")
    imei_script_path: str = environ.get("IMEI_SCRIPT_PATH")

settings = Settings()
