from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey
from backend.security.auth import validate_api_key
from backend.api_v1.commands.imei.imei_checker import check_imei_by_number
from backend.schema.imei import ImeiInput, ImeiResponse

router = APIRouter()


@router.post("/check-imei")
async def check_imei(
    user_input: ImeiInput, api_key: APIKey = Depends(validate_api_key)
) -> ImeiResponse:
    response = await check_imei_by_number(user_input.imei, user_input.email_address)
    return response