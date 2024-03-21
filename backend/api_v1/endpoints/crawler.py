from fastapi import APIRouter
from backend.schema.crawler import CrawlerInputLinks, CrawlerInputKeyword
from backend.api_v1.commands.crawler_apk.apk_font_extractor import (
    collect_links_by_author,
)
from backend.api_v1.commands.crawler_apk.messages import (
    keyword_mail_response,
    link_mail_response,
)
from backend.schema.mail import RequestAccepted
from backend.tasks.task import run_custom_task


router = APIRouter()


@router.post("/process-from-links")
async def process_from_links(crawler_input: CrawlerInputLinks) -> RequestAccepted:
    mail_response = link_mail_response()
    run_custom_task.delay(
        target_email=str(crawler_input.target_email),
        urls=crawler_input.links,
        mail_response=mail_response,
    )
    return RequestAccepted(data="Request is being processed.")


@router.post("/process-from-keywords")
async def process_from_keyword(crawler_input: CrawlerInputKeyword) -> RequestAccepted:
    links = collect_links_by_author(crawler_input.keywords)
    if not links:
        return RequestAccepted(data="No links found.")

    mail_response = keyword_mail_response(crawler_input.keywords)
    run_custom_task.delay(
        target_email=str(crawler_input.target_email),
        urls=links,
        mail_response=mail_response,
    )
    return RequestAccepted(data="Request is being processed.")
