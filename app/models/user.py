
from pydantic.main import BaseModel


class User(BaseModel):
    email: str
    tel: str
    name: str
    surname: str
    session_token: str

class patch_user(BaseModel):
    name: str
    surname: str
    tel: str
    email: str
