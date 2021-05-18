from typing import Optional
from pydantic.main import BaseModel


class User(BaseModel):
    tel: str
    name: str
    surname: str
    avatar:str
    session_token: str
    view:int
    is_moder:bool

class patch_user(BaseModel):
    name: Optional[str] = ""
    surname: Optional[str] = ""
    tel: Optional[str] = ""
    email: Optional[str] = ""
    companyName: Optional[str] = ""
    workDate:Optional[int] = 0
    specialization:Optional[str] = ""
    about:Optional[str] = ""
    website:Optional[str] = ""


class patch_user_password(BaseModel):
    old_password:str
    new_password: str
 
class view_tel(BaseModel):
    id:str