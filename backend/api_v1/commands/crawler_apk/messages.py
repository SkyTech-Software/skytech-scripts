def keyword_mail_response(keywords: list[str]) -> str:
    return f"""Dzień dobry,
W załączniku przesyłamy .zip z fontami od Deweloperów: {', '.join([item for item in keywords])}


Pozdrawiamy
Zespół SkyTech
"""


def link_mail_response() -> str:
    return """Dzień dobry,
W załączniku przesyłamy .zip z fontami z aplikacji z załącznego pliku .csv

Pozdrawiamy
Zespół Skytech
    """
