import smtplib
from backend.core.config import settings
from backend.schema.mail import Mail
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from smtplib import SMTPException
from fastapi import HTTPException
from email import encoders
from fastapi import UploadFile


async def send_mail(target_email: str, subject: str, message: str, file: UploadFile | None = None) -> dict:
    server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
    server.starttls()
    server.login(settings.USERNAME, settings.PASSWORD)

    msg = MIMEMultipart()
    msg["From"] = settings.USERNAME
    msg["To"] = target_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    if file:
        part = MIMEBase("application", file.content_type)
        part.set_payload(await file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={file.filename}")
        msg.attach(part)

    try:
        server.sendmail(settings.USERNAME, target_email, msg.as_string())
        return True

    except SMTPException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email. Error {e}")

    finally:
        server.quit()