from pydantic import BaseModel
from datetime import datetime


class CreateLicense(BaseModel):
    license_key: str
    mac_address: str


class CreateLicenseKeyInput(BaseModel):
    exp_date: str | None


class CreateLicenseKey(CreateLicense):
    mac_address: str | None
    is_active: bool = True
    activation_date: datetime | None
    exp_date: str | None
