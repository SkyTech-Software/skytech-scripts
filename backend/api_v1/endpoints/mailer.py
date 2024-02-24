from fastapi import APIRouter, Depends
from backend.api_v1.commands.mailer import send_mail
from fastapi import UploadFile
from backend.schema.mail import MailResponse

router = APIRouter()


@router.post("/send-mail")
async def send_email(
    target_email: str, subject: str, message: str, file: UploadFile = None
) -> MailResponse:
    response = await send_mail(
        target_email=target_email, subject=subject, message=message, file=file
    )
    return response