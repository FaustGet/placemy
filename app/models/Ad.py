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


class Delete_offer(BaseModel):
    id:str

class activ_offer(BaseModel):
    id:str
    state:int
    note:Optional[str] = ""

class Offer_patch(BaseModel):
    id:str 
    offerObject: Optional[dict] = {}
    offerPrice: Optional[dict] = {}
    description: str 
    photos: list 
    title:str 