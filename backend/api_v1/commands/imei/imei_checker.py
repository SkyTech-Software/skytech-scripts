from backend.api_v1.commands.imei import orange, tmobile, plus
from backend.schema.imei import ImeiResponse

async def check_imei_by_number(imei: int, target_email: str):
    orange_response = orange.send_request_to_orange(imei, target_email)
    tmobile_response = tmobile.send_request_to_tmobile(imei, target_email)
    plus_response = plus.send_request_to_plus(imei, target_email)
    return ImeiResponse(orange=orange_response, tmobile=tmobile_response, plus=plus_response)