import requests

def send_request_to_orange(imei: int, email: str) -> bool:
    try:
        response_orange = requests.post(
            url="https://www.orange.pl/hapi/pwa/v1/notification/email",
            json={
                "data": {
                    "deviceNumberImei": imei,
                    "email": email,
                    "consent-imei-1": True,
                },
                "type": "DEVICE_IMEI",
                "formComponentId": "imei_form",
            },
        )
        response_orange.raise_for_status()
        return True
    except requests.RequestException as e:
        # log error
        return False