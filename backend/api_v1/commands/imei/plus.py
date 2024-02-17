import requests

def send_request_to_plus(imei, email):
    try:
        plus_email = email.replace("@", "%40")
        response_plus = requests.post(
            url="https://www.plus.pl/formularze/formularz-imei?p_p_id=contactformportlet_WAR_frontend_INSTANCE_formconsultantimei00"
            "&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&_contactformportlet_WAR_frontend_INSTANCE"
            f"_formconsultantimei00_action=saveContact&event_type=imei_form&imei={imei}&email={plus_email}&mail_title=Formularz+IMEI"
        )
        response_plus.raise_for_status()
        return True

    except requests.RequestException as e:
        # Log error
        return False