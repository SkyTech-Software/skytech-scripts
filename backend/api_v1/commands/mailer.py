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
from backend.schema.mail import MailResponse


async def send_mail(target_email: str, subject: str, message: str, file: UploadFile | None = None) -> dict:
    server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
    server.starttls()
    server.login(settings.mailer_username, settings.mailer_password)

    msg = MIMEMultipart()
    msg["From"] = settings.mailer_username
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
        server.sendmail(settings.mailer_username, target_email, msg.as_string())
        
    except SMTPException as e:
        return MailResponse(success=False, data="Failed to send an email.")

    finally:
        server.quit()
        return MailResponse(success=True, data="Mail has been sent.")
