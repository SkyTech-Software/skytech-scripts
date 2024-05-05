from backend.core.celery_config import celery
from backend.api_v1.commands.mailer.mailer import send_mail
from backend.api_v1.commands.crawler_apk.apk_font_extractor import (
    run_extractor,
    collect_links_by_author,
)
from typing import Any
from backend.api_v1.commands.crawler_apk.mail_responses import generate_mail_body_apk
from backend.api_v1.commands.aws.upload_file import upload_file_to_aws_storage
from uuid import uuid4
from backend.db.logging import add_log
from time import time
from functools import wraps
from datetime import datetime


def log_task(func):  # type: ignore
    @wraps(func)
    def wrapper(self, *args, **kwargs):  # type: ignore
        start_time = time()
        add_log(
            task_id=self.request.id,
            task_name=self.name,
            task_response="Task execution started.",
            task_execution_time=None,
            task_error_message=None,
        )
        try:
            result = func(self, *args, **kwargs)
            task_execution_time = time() - start_time
            add_log(
                task_id=self.request.id,
                task_name=self.name,
                task_response="Task execution ended.",
                task_execution_time=task_execution_time,
                task_error_message=None,
            )
            return result
        except Exception as e:
            task_execution_time = time() - start_time
            add_log(
                task_id=self.request.id,
                task_name=self.name,
                task_response="Task failed.",
                task_execution_time=task_execution_time,
                task_error_message=str(e),
            )
            raise e

    return wrapper


@celery.task(bind=True, name="analyze_apk_from_links", queue="tasks", serializer="json")  # type: ignore
@log_task  # type: ignore
def analyze_apk_from_links(self: Any, target_email: str, links: list[str]) -> bool:

    zip_file, csv_file = run_extractor([{link: link} for link in links])
    aws_storage_link = upload_file_to_aws_storage(zip_file, f"Fonts_{uuid4()}.zip")
    mail_message = generate_mail_body_apk(aws_storage_link)
    current_time = datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
    send_mail(
        target_email=target_email,
        subject="Fonts Extractor",
        message=mail_message,
        file_content_type="text/csv",
        file_content=csv_file,
        file_name=f"Summary_{current_time}.csv",
    )
    return True


@celery.task(bind=True, name="analyze_apk_from_keywords", queue="tasks", serializer="json")  # type: ignore
@log_task  # type: ignore
def analyze_apk_from_keywords(
    self: Any, target_email: str, keywords: list[str]
) -> bool:
    urls = collect_links_by_author(keywords)
    zip_file, csv_file = run_extractor(urls)
    aws_storage_link = upload_file_to_aws_storage(zip_file, f"Fonts_{uuid4()}.zip")
    mail_message = generate_mail_body_apk(aws_storage_link)

    current_time = datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
    send_mail(
        target_email=target_email,
        subject="Fonts Extractor",
        message=mail_message,
        file_content_type="text/csv",
        file_content=csv_file,
        file_name=f"Summary_{current_time}.csv",
    )

    return True
