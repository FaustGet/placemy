from pydantic.main import BaseModel
from typing import Optional


class Place_an_ad(BaseModel):
    offerType: dict
    offerMap: dict
    offerObject: dict
    offerPrice: dict
    offerPhothos: list
    offerDescription: str

class Test_celery(BaseModel):
    name:str
    q:int