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


async def get_current_session_user(token):
    try:
        token = token.replace('"',"")
        payload = jwt.decode(token, Authentication_config.SECRET_KEY, algorithms=[Authentication_config.ALGORITHM])
        email = payload.get("email")
    except JWTError:
        raise HTTPException(status_code=401)
    if email is None:
        raise HTTPException(status_code=401)
    user = await db.users.find_one({'email': email})
    if not user:
        user = await db.moderators.find_one({'email': email})
        print("moder-",user)
        user['_id'] = 'moderator'
    return user





