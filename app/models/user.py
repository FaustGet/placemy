
from pydantic.main import BaseModel


class User(BaseModel):
    email: str
    tel: str
    name: str
    surname: str
    patronymic: str
    session_token: str
