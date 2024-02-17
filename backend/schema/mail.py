from pydantic import BaseModel


class Mail(BaseModel):
    to_email: str
    subject: str
    message: str