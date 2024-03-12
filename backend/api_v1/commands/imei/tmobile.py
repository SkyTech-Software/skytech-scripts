import requests


def send_request_to_tmobile(imei: int, email: str) -> bool:
    try:
        response_tmobile = requests.post(
            timeout=60,
            url="https://tmobile-actions-api.smvg.pl/lead",
            json={"action_id": 595, "email": email, "imei": imei, "zgoda": "17"},
        )
        response_tmobile.raise_for_status()
        return True
    except requests.RequestException:
        return False
