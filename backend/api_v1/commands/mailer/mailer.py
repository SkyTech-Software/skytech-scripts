import smtplib
from backend.core.config import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTPException
from backend.schema.mail import MailResponse
from email.mime.base import MIMEBase
from email import encoders


def send_mail(
    target_email: str,
    subject: str,
    message: str,
    file_content_type: str | None = None,
    file_content: bytes | None | str = None,
    file_name: str | None = None,
) -> MailResponse:
    server = smtplib.SMTP(settings.smtp_server, int(settings.smtp_port))
    server.starttls()
    server.login(settings.mailer_username, settings.mailer_password)

    msg = MIMEMultipart()
    msg["From"] = settings.mailer_username
    msg["To"] = target_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    if file_content:
        part = MIMEBase("application", f"{file_content_type}")
        part.set_payload(file_content)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={file_name}")
        msg.attach(part)

    try:
        server.sendmail(settings.mailer_username, target_email, msg.as_string())
    except SMTPException as error:
        return MailResponse(
            success=False, data=f"Failed to send an email. Error:{error}"
        )

    finally:
        server.quit()

    return MailResponse(success=True, data="Mail has been sent.")
