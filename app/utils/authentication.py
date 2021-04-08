import random
from datetime import timedelta, datetime
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from config.authentication import *
from config.mongodb import db


async def create_access_token(data: dict, expires_delta: Optional[int] = 1000000):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Authentication_config.SECRET_KEY, algorithm=Authentication_config.ALGORITHM)
    return encoded_jwt

async def check_activ_user_form_emailhash(token:str):
    try:
        payload = jwt.decode(token, Authentication_config.SECRET_KEY, algorithms=[Authentication_config.ALGORITHM])
        email = payload.get("email")
        cod = payload.get("code")
        exp = payload.get("exp")
        if int(datetime.today().timestamp()) > exp:
            raise HTTPException(status_code=409)
        user = await db.users.find_one({'email':email})
        if not user:
            raise HTTPException(status_code=404)
        if user['code_activation'] == cod:
            db.users.update_one({'email':email},{"$set":{"is_activ":True,"code_activation":""}})
        else:
            raise HTTPException(status_code=409)
        return True
    except:
        raise HTTPException(status_code=409)

async def get_current_session_user(token):
    try:
        payload = jwt.decode(token, Authentication_config.SECRET_KEY, algorithms=[Authentication_config.ALGORITHM])
        email = payload.get("email")
    except JWTError:
        raise HTTPException(status_code=401)
    if email is None:
        raise HTTPException(status_code=401)
    users_collection = db.users
    #проверка на клиента
    user = await users_collection.find_one({'email': email})
    return user

async def check_auth_user(request: Request):
    try:
        if (not request.cookies) or ('session_token' not in request.cookies):
            raise HTTPException(status_code=401)
        user = await get_current_session_user(request.cookies.get('session_token'))
        return user
    except:
        raise HTTPException(status_code=401)