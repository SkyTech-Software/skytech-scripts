from pydantic import BaseModel


class Mail(BaseModel):
    to_email: str
    subject: str
    message: str


class MailResponse(BaseModel):
    success: bool
    data: str