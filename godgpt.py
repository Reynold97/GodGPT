from helper.classes import Role, Message
from helper.openai_api import create_message
from helper.twilio_api import send_message
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse
from typing import Dict


load_dotenv()

app = FastAPI()


@app.get('/')
async def home():
    return {"Cheking" : "OK", "godgpt version" : "0.5.0"}


@app.post("/new_message")
def new_message(input_messages : list[Message]):
    
    result = create_message(input_messages)
    
    return Message(role=Role.assistant, content=result)



@app.post('/twilio/new_message', response_class=PlainTextResponse)
async def twiliomessage(request: Request) -> None:
    
    form_data: Dict[str, str] = await request.form()
    input_message = form_data.get('Body')
    sender_id = form_data.get('From')

    message = [
    Message(role=Role.user, content=input_message),
    ]

    result = create_message(message)
    
    send_message(sender_id, result)
  