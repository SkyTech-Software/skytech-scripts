from fastapi import APIRouter
from backend.schema.crawler import CrawlerInputLinks, CrawlerInputKeyword
from backend.api_v1.commands.crawler_apk.apk_font_extractor import (
    run_extractor,
    collect_links_by_author,
)
from backend.api_v1.commands.crawler_apk.messages import (
    keyword_mail_response,
    link_mail_response,
)
from backend.api_v1.commands.mailer.mailer import send_mail
from backend.schema.mail import MailResponse

router = APIRouter()


@router.post("/process-from-links")
async def process_from_links(crawler_input: CrawlerInputLinks) -> MailResponse:
    zip_file = await run_extractor(crawler_input.links)
    return send_mail(
        target_email=crawler_input.target_email,
        subject="Fonts Extractor",
        message=link_mail_response(),
        file_content=zip_file,
        file_content_type="zip",
        file_name="Fonts.zip",
    )


@router.post("/process-from-keyword")
async def process_from_keyword(crawler_input: CrawlerInputKeyword) -> MailResponse:
    links = collect_links_by_author(crawler_input.keyword)
    zip_file = await run_extractor(links)
    return send_mail(
        target_email=crawler_input.target_email,
        subject="Fonts Extractor",
        message=keyword_mail_response(crawler_input.keyword),
        file_content=zip_file,
        file_content_type="zip",
        file_name="Fonts.zip",
    )
