import os
import requests
from dotenv import load_dotenv

load_dotenv()

SOLAPI_API_KEY = os.getenv("SOLAPI_API_KEY")
SOLAPI_API_SECRET = os.getenv("SOLAPI_API_SECRET")
SOLAPI_FROM_NUMBER = os.getenv("SOLAPI_FROM_NUMBER")


def send_sms(to, content):
    url = "https://api.solapi.com/messages/v4/send"
    data = {
        "message": {
            "to": to,
            "from": SOLAPI_FROM_NUMBER,
            "text": content
        }
    }
    response = requests.post(
        url,
        json=data,
        auth=(SOLAPI_API_KEY, SOLAPI_API_SECRET)
    )
    return response.json()
