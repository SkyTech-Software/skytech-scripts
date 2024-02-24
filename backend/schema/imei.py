from pydantic import BaseModel


class ImeiInput(BaseModel):
    imei: int
    email_address: str


class ImeiResponse(BaseModel):
    orange: bool
    tmobile: bool
    plus: bool
