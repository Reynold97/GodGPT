from pydantic import BaseModel
from enum import Enum

class Role(Enum):
    user = "user"
    system = "system"
    assistant = "assistant"
    

class Message(BaseModel):
    role : Role
    content : str