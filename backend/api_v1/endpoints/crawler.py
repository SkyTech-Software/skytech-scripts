from fastapi import APIRouter
from backend.schema.crawler import CrawlerInputLinks, CrawlerInputKeyword
from backend.api_v1.commands.crawler_apk.apk_font_extractor import run_extractor
from backend.api_v1.commands.mailer.mailer import send_mail
from backend.schema.mail import MailResponse

router = APIRouter()


@router.post("/process-from-links")
async def process_from_links(crawler_input: CrawlerInputLinks) -> MailResponse:
    zip_file = run_extractor(crawler_input.links)
    return send_mail(
        target_email=crawler_input.target_email,
        subject="Fonts Extractor",
        message="Please find attached .zip file.",
        file_content=zip_file,
        file_content_type="zip",
        file_name="Fonts.zip",
    )


# PLACEHOLDER #
@router.post("/process-from-keyword")
async def process_from_keyword(crawler_input: CrawlerInputKeyword) -> int:
    # TODO: logic keyword
    return 200
