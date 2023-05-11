import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def send_message(to: str, message: str):
    print("mandar sms")
    message = client.messages.create(
        from_=os.getenv('FROM'),
        body=message,
        to=to
    )
