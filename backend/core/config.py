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
    aws_access_point_alias: str = environ["AWS_ACCESS_POINT_ALIAS"]
    aws_access_key_id: str = environ["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key: str = environ["AWS_SECRET_ACCESS_KEY"]
    aws_region: str = environ["AWS_REGION"]
    aws_bucket_name: str = environ["AWS_BUCKET_NAME"]
    aws_link_exp_time: str = environ["AWS_LINK_EXP_TIME"]
    pg_database_url: str = environ["PG_DATABASE_URL"]


settings = Settings()
