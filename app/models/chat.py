from typing import Optional

from pydantic import BaseModel


class Open_chat(BaseModel):
    id_offer:str

class Get_messages(BaseModel):
    id_chat:str
