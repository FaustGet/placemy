from typing import Optional
from pydantic.main import BaseModel


class Signin(BaseModel):
    tel: str
    password: str

class Signup(BaseModel):
    _id:Optional[str] = ""
    account_type:Optional[str] = ""
    name: Optional[str] = ""
    surname: Optional[str] = ""
    tel: Optional[str] = ""
    companyName: Optional[str] = ""
    workDate:Optional[int] = 0
    specialization:Optional[str] = ""
    about:Optional[str] = ""
    website:Optional[str] = ""
    password: Optional[str] = ""


class Activ_user(BaseModel):
    tel:str
    code:str

class Reset_pass(BaseModel):
    tel:str

class Restore_pass(BaseModel):
    tel:str
    code:str
    password:str

class Complaint(BaseModel):
    id_user:str
    title:str
    text:str