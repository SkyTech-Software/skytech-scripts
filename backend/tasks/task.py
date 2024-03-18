from backend.core.celery_config import celery
from backend.api_v1.commands.mailer.mailer import send_mail
from backend.api_v1.commands.crawler_apk.apk_font_extractor import run_extractor
from typing import Any

@celery.task(bind=True, name="run_custom_task", queue="tasks", serializer='json') # type: ignore
def run_custom_task(self: Any, target_email:str, urls: list[str], mail_response: str) -> bool:
    zip_file = run_extractor(urls)
    send_mail(
        target_email=target_email,
        subject="Fonts Extractor",
        message=mail_response,
        file_content=zip_file,
        file_content_type="zip",
        file_name="Fonts.zip",
    )
    
    return True


