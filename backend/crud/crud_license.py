from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from backend.crud.base import CRUDBase
from backend.db.models import LicenseBase
from fastapi.responses import JSONResponse


class CRUDLicense(CRUDBase[LicenseBase, LicenseBase, LicenseBase]):

    def activate_license(self, db: Session, license_key: str, mac_address: str) -> Any:
        license_obj = (
            db.query(LicenseBase)
            .filter(
                LicenseBase.license_key == license_key,
                LicenseBase.is_active == True,
                LicenseBase.mac_address.is_(None),
            )
            .first()
        )

        if license_obj:
            license_obj.mac_address = mac_address
            license_obj.activation_date = datetime.now().strftime("%Y-%m-%d :%H:%M:%S")
            db.add(license_obj)
            db.commit()
            db.refresh(license_obj)
            return JSONResponse(
                status_code=200, content={"message": "The product has been activated."}
            )
        else:
            return JSONResponse(
                status_code=404, content={"message": "Invalid License Key."}
            )

    def check_license(self, db: Session, mac_address: str) -> Any:
        license_obj = (
            db.query(LicenseBase)
            .filter(
                LicenseBase.license_key is not None,
                LicenseBase.is_active == True,
                LicenseBase.mac_address == mac_address,
                LicenseBase.exp_date > datetime.now(),
            )
            .first()
        )
        return license_obj


crud_license = CRUDLicense(LicenseBase)
