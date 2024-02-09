from datetime import datetime
from sqlmodel import Field, SQLModel


class LicenseBase(SQLModel, table=True):
    __tablename__ = "imei_app"
    id: int = Field(unique=True, index=True, primary_key=True)
    mac_address: str | None
    license_key: str
    is_active: bool = True
    activation_date: datetime | None
    exp_date: datetime | None
