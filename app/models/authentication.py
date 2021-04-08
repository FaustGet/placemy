
from pydantic.main import BaseModel


class Signin(BaseModel):
    email: str
    password: str

class Signup(BaseModel):
    name: str
    surname: str
    patronymic: str
    tel: str
    email: str
    password: str

class Activ_user(BaseModel):
    token:str