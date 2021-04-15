from typing import Optional

from pydantic import BaseModel


class Filter_offers(BaseModel):
    address: Optional[str] = ""
    deals: str
    objects: str
    priceFrom: Optional[int] = 0
    priceTo: Optional[int] = 0
    repair: Optional[str] = ""
    rooms: Optional[str] = ""
    sizeFrom: Optional[int] = 0
    sizeTo: Optional[int] = 0
    typeBuilding: Optional[str] = ""
    typeCommercy: Optional[str] = ""
    typeGround: Optional[str] = ""
