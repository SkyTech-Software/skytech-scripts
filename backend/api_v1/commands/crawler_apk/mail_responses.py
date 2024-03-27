from backend.core.config import settings


def generate_mail_body_apk(link: str) -> str:
    return f"""Dzień dobry,

Mamy przyjemność poinformować, że przygotowane pliki fontów są już gotowe do pobrania. Zachęcamy do skorzystania z poniższego linku, który będzie aktywny przez najbliższe {int(int(settings.aws_link_exp_time)/60/60)} godzin od momentu otrzymania tej wiadomości:

Link do pobrania plików: {link}

Prosimy o pobranie plików w wyznaczonym czasie, ponieważ po tym czasie nie będzie to możliwe. Jeśli napotkają Państwo jakiekolwiek problemy podczas pobierania lub mają dodatkowe pytania, prosimy o kontakt. Nasz zespół jest do Państwa dyspozycji i chętnie udzieli potrzebnej pomocy.

Z wyrazami szacunku
Zespół SkyTech
"""
