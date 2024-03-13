from pydantic import BaseModel


class CrawlerInputLinks(BaseModel):
    target_email: str
    links: list[str]


class CrawlerInputKeyword(BaseModel):
    target_email: str
    keyword: str
