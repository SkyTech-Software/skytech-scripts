
from backend.api_v1.commands.mailer import send_mail
import subprocess
from backend.core.config import settings

async def send_request_to_play(imei, target_email):
    try:
        result = subprocess.run(['python', settings.imei_script_path, str(imei)], capture_output=True, text=True, check=True)
        response = result.stdout
        if not response:
            response = "Could not check Play automatically: https://www.play.pl/uslugi/sprawdz-wlasciciela-telefonu-imei"
        mail_sent = await send_mail(target_email=target_email, subject="Play IMEI", message=response, file=None)
        if mail_sent:
            return True
    except subprocess.CalledProcessError as e:
        return False
    
   