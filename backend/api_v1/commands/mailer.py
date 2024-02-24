import smtplib
from backend.core.config import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTPException
from backend.schema.mail import MailResponse


async def send_mail(target_email: str, subject: str, message: str) -> MailResponse:
    server = smtplib.SMTP(settings.smtp_server, int(settings.smtp_port))
    server.starttls()
    server.login(settings.mailer_username, settings.mailer_password)

    msg = MIMEMultipart()
    msg["From"] = settings.mailer_username
    msg["To"] = target_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server.sendmail(settings.mailer_username, target_email, msg.as_string())

    except SMTPException as error:
        return MailResponse(
            success=False, data=f"Failed to send an email. Error:{error}"
        )

    finally:
        server.quit()
        return MailResponse(success=True, data="Mail has been sent.")
