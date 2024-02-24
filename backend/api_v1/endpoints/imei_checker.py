from fastapi import APIRouter
from backend.api_v1.commands.imei.imei_checker import check_imei_by_number
from backend.schema.imei import ImeiInput, ImeiResponse

router = APIRouter()


@router.post("/check-operators", response_model=ImeiResponse)
async def check_operators(user_input: ImeiInput) -> ImeiResponse:
    response = await check_imei_by_number(user_input.imei, user_input.email_address)
    return response
