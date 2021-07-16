from pydantic.main import BaseModel
from typing import Optional

class OfferData(BaseModel):
    name:str
    workDate:str
    workTime:str
    specialization:str
    listPhotos:list
    city:str
    description:str




class Create_services(BaseModel):
    offerData:OfferData
    storeService:list


class Patch_offerData(BaseModel):
    name:Optional[str]=""
    workDate:Optional[str]=""
    workTime:Optional[str]=""
    specialization:Optional[str]=""
    listPhotos:Optional[list] = []
    city:Optional[str] = ""
    description:Optional[str] = ""

class Patch_services(BaseModel):
    id:Optional[str]=""
    offerData:OfferData
    storeService:Optional[list]=[]


class Activ_services(BaseModel):
    id:str
    state:int
    note:Optional[str] = ""

class Delete_services(BaseModel):
    id:str