from pydantic import BaseModel


class del_file(BaseModel):
    name: str

class Filter_offers(BaseModel):
    searchData: dict