import string
import secrets


def generate_license_key():
    alphabet = string.ascii_letters + string.digits
    license_key = "".join(secrets.choice(alphabet) for _ in range(20))
    formatted_key = "-".join(
        [license_key[i : i + 5] for i in range(0, len(license_key), 5)]
    )
    return formatted_key
