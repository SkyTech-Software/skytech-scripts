from fastapi import APIRouter, Depends
from backend.db.session import get_db
from backend.crud.crud_license import crud_license
from backend.schemas.license import (
    CreateLicense,
    CreateLicenseKey,
    CreateLicenseKeyInput,
)
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from backend.api_v1.commands.utils import generate_license_key
from datetime import datetime

router = APIRouter()


@router.post("/create_license_key")
async def create_license_key(
    license_key_input: CreateLicenseKeyInput, db: Session = Depends(get_db)
) -> JSONResponse:
    license_key = generate_license_key()
    license_key = crud_license.create(
        db=db,
        obj_in=CreateLicenseKey(
            license_key=license_key,
            mac_address=None,
            is_active=True,
            activation_date=None,
            exp_date=license_key_input.exp_date,
        ),
    )
    return JSONResponse(
        status_code=200,
        content={
            "message": f"New license key [{license_key.license_key}] has been created."
        },
    )


@router.put("/activate_license")
async def activate_license(
    license_in: CreateLicense, db: Session = Depends(get_db)
) -> JSONResponse:
    license_response = crud_license.activate_license(
        db=db, license_key=license_in.license_key, mac_address=license_in.mac_address
    )
    return license_response


@router.get("/check_license/{mac_address}")
async def check_license(
    mac_address: str, db: Session = Depends(get_db)
) -> JSONResponse:
    license = crud_license.check_license(db=db, mac_address=mac_address)
    if license:
        return JSONResponse(status_code=200, content={"message": "License is valid."})
    return JSONResponse(
        status_code=410, content={"message": "License key is no longer valid."}
    )
