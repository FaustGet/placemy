from typing import Optional
from pydantic.main import BaseModel


class Signin(BaseModel):
    email: str
    password: str

class Signup(BaseModel):
    name: str
    surname: str
    tel: str
    email: str
    password: str


class Activ_user(BaseModel):
    token:str

class Reset_pass(BaseModel):
    email:str

class Restore_pass(BaseModel):
    token:str
    password:str

