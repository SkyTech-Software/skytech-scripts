from celery import Celery # type: ignore
from backend.core.config import settings

celery = Celery("backend", include=["backend.tasks.task"])
celery.config_from_object("backend.core.celery_config")


celery.conf.broker_url = settings.celery_broker_url
celery.conf.result_backend = settings.celery_result_backend_url
celery.conf.broker_connection_retry_on_startup = False
celery.conf.accept_content = ['application/json', 'application/x-python-serialize']
