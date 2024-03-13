from fastapi import APIRouter
from backend.api_v1.commands.mailer.mailer import send_mail
from backend.schema.mail import MailResponse, Mail

router = APIRouter()


@router.post("/send-mail", response_model=MailResponse)
async def send_email(mail_input: Mail) -> MailResponse:
    return send_mail(
        target_email=mail_input.to_email,
        subject=mail_input.subject,
        message=mail_input.message,
    )
