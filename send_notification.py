from env_vars import env
import json
import requests

async def send_notification(kwargs, message):
    print("Sending notification 1st time....")
    r = requests.get(
            "http://api.sparrowsms.com/v2/sms/",
            params={'token' : env.sparrow_token,
                  'from'  : env.sparrow_from,
                  'to'    : env.sparrow_to,
                  'text'  : f"Warning: Critical \nOrganization: {kwargs['organization']} \nFreeze: {kwargs['freeze_id']} \nTemperature: {json.loads(message.payload.decode())['temp']} degree Celsius."})

    status_code = r.status_code
    response = r.text
    response_json = r.json()
    print(status_code)
    print(response)
    print(response_json)
    print("success")



