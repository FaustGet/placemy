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
    expire = datetime.now() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Authentication_config.SECRET_KEY, algorithm=Authentication_config.ALGORITHM)
    return encoded_jwt

async def check_activ_user_form_emailhash(token:str,pas = ""):
    try:
        payload = jwt.decode(token, Authentication_config.SECRET_KEY, algorithms=[Authentication_config.ALGORITHM])
        email = payload.get("email")
        cod = payload.get("code")
        exp = payload.get("exp")
        if int(datetime.today().timestamp()) > exp:
            return Response(status_code=482)
        user = await db.users.find_one({'email':email})
        if not user:
            raise HTTPException(status_code=404)
        if user['is_activ'] == True and user['code_activation'] == cod:
            db.users.update_one({'email':email},{"$set":{"password":pas,"code_activation":""}})
            return True
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
        exp = payload.get("exp")
        if int(datetime.today().timestamp()) > exp:
            return Response(status_code=482)
    except JWTError:
        raise HTTPException(status_code=401)
    if email is None:
        raise HTTPException(status_code=401)

    users_collection = db.users
    user = await users_collection.find_one({'email': email})
    return user

async def check_auth_user(request: Request,access = 0):
    try:
        if 'session_token' in request.cookies:
            token = request.cookies.get('session_token')
        else:
            if 'authorization' in request.headers:
                 token = request.headers['authorization'][7:]
        user = await get_current_session_user(token)

        if access == 1:
           if not user:
               user = await get_current_moderator(token)
               if user['_id'] in Moderotor.id:
                  user['_id'] = 'moderator'
        return user
    except:
        raise HTTPException(status_code=401)

async def check_auth_ret_user(request: Request):
    try:
        if 'session_token' in request.cookies:
            token = request.cookies.get('session_token')
        else:
            if 'authorization' in request.headers:
                 token = request.headers['authorization'][7:]
        payload = jwt.decode(token, Authentication_config.SECRET_KEY, algorithms=[Authentication_config.ALGORITHM])
        email = payload.get("email")
        exp = payload.get("exp")
        if int(datetime.today().timestamp()) > exp:
            return Response(status_code=482)

        if email is None:
            return -1
        user = await db.users.find_one({'email': email})
        if user:
            return True
        return -1
    except:
        return -1 

async def get_current_moderator(token):
    try:
        payload = jwt.decode(token, Authentication_config.SECRET_KEY, algorithms=[Authentication_config.ALGORITHM])
        email = payload.get("email")
        exp = payload.get("exp")
        if int(datetime.today().timestamp()) > exp:
            return Response(status_code=482)
    except JWTError:
        raise HTTPException(status_code=401)
    if email is None:
        raise HTTPException(status_code=401)
    user = await db.moderators.find_one({'email': email})
    return user

async def check_auth_moderator(request: Request):
    try:
        if 'session_token' in request.cookies:
            token = request.cookies.get('session_token')
        else:
            if 'authorization' in request.headers:
                 token = request.headers['authorization'][7:]
        user = await get_current_moderator(token) 
        if user['_id'] in Moderotor.id:
            return user
        else:
            raise HTTPException(status_code=403)
    except:
        raise HTTPException(status_code=403)

