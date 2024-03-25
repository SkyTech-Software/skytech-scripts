from fastapi import APIRouter
from backend.schema.crawler import CrawlerInputLinks, CrawlerInputKeyword
from backend.schema.mail import RequestAccepted
from backend.tasks.task import analyze_apk_from_links, analyze_apk_from_keywords

router = APIRouter()


@router.post("/process-from-links")
async def process_from_links(crawler_input: CrawlerInputLinks) -> RequestAccepted:
    analyze_apk_from_links.delay(
        target_email=str(crawler_input.target_email),
        links=crawler_input.links,
    )
    return RequestAccepted(data="Request is being processed.")


@router.post("/process-from-keywords")
async def process_from_keyword(crawler_input: CrawlerInputKeyword) -> RequestAccepted:
    analyze_apk_from_keywords.delay(
        target_email=str(crawler_input.target_email), keywords=crawler_input.keywords
    )
    return RequestAccepted(data="Request is being processed.")
