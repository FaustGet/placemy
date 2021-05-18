from typing import Optional
from pydantic.main import BaseModel


class Account(BaseModel):
    type:str
    page: Optional[int] = 1
    

class Review(BaseModel):
    id:str
    text: str
    value: int