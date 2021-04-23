from pydantic.main import BaseModel
from typing import Optional


class Place_an_ad(BaseModel):
    offerType: dict
    offerMap: dict
    offerObject: dict
    offerPrice: dict
    offerDescription: str
    offerPhothos: list

class Test_celery(BaseModel):
    name:str
    q:int

class aciv_offer(BaseModel):
    id:str