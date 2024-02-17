from backend.api_v1.commands.imei import orange, tmobile, play, plus
from backend.schema.imei import ImeiResponse

async def check_imei_by_number(imei: int, target_email: str):
    # orange_response = orange.send_request_to_orange(imei, target_email)
    # tmobile_response = tmobile.send_request_to_tmobile(imei, target_email)
    play_response = play.send_request_to_play(imei, target_email)
    print(play_response)
    # plus_response = plus.send_request_to_plus(imei, target_email)
    return ImeiResponse(orange=True, tmobile=True, play=play_response, plus=True)