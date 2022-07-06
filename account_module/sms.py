import json

import requests

def send_otp_sms(phone_number, otp):
    header = {
        'ACCEPT': 'application/json',
        'X-API-KEY': '8kMZ6QXJzza0NtPvNXX8ubVCZX1dvTvV9e3h69hT9w5KeKBlfgrpkdgZ63nzKJS4'
    }
    body = {
            "mobile": phone_number,
            "templateId": 901688,
            "parameters": [
                {
                    "name": "CODE",
                    "value": otp
                }
            ]
        }

    url = 'https://api.sms.ir/v1/send/verify'
    response = requests.post(url=url, json=body, headers=header)
    res = json.loads(response.text)
    status = res['status']
    return status

send_otp_sms('09039202857','165462')