from typing import Optional

from pydantic import BaseModel


class Filter_offers(BaseModel):
    address: Optional[str] = ""
    deals: Optional[dict]={}
    objects: Optional[dict]={}
    priceFrom: Optional[int] = 0
    priceTo: Optional[int] = 0
    repair: Optional[dict]={}
    rooms: Optional[dict]={}
    sizeFrom: Optional[int] = 0
    sizeTo: Optional[int] = 0
    typeBuilding: Optional[dict]={}
    typeCommercy: Optional[dict]={}
    typeGround: Optional[dict]={}
    cities: Optional[dict]={}
    page: Optional[int] = 1

class List_filter_offers(BaseModel):
    id:str
    title:str
    address:str
    price:int
    price_m2: float
    description:str
    images:list
    is_agent:bool
