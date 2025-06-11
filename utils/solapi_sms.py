import os
import requests
from dotenv import load_dotenv
from solapi import SolapiMessageService
from solapi.model import RequestMessage

load_dotenv()

SOLAPI_API_KEY = os.getenv("SOLAPI_API_KEY")
SOLAPI_API_SECRET = os.getenv("SOLAPI_API_SECRET")
SOLAPI_FROM_NUMBER = os.getenv("SOLAPI_FROM_NUMBER")

message_service = SolapiMessageService(
    api_key=SOLAPI_API_KEY,
    api_secret=SOLAPI_API_SECRET
)

def send_sms(to, content):
    try:
        message = RequestMessage(
            from_=SOLAPI_FROM_NUMBER.replace("-", ""),
            to=to.replace("-", ""),
            text=content
        )

        response = message_service.send(message)
        return {
            "success": True,
            "group_id": response.group_info.group_id,
            "requested": response.group_info.count.total,
            "success_count": response.group_info.count.registered_success,
            "fail_count": response.group_info.count.registered_failed
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }