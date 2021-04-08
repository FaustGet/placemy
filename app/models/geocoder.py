from pydantic.main import BaseModel


class Geocoder_reverse(BaseModel):
    x:float
    y:float

class Geocoder_point(BaseModel):
    map_address:str
