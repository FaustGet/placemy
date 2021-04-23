import uuid
import random
from starlette.requests import Request
from fastapi import APIRouter, HTTPException,Response
from config import server
from config.authentication import *
from config.mongodb import db
from jose import JWTError, jwt
from models.authentication import *
from models.user import *

from utils.authentication import *
from utils.email import send_mes

router = APIRouter(prefix=server.Server_config.prefix,
                   responses = server.Server_config.responses,
                   tags=['authentication'])

@router.post("/auth_signin")
async def login(signin:Signin,response:Response):
    user = await db.users.find_one({'email':signin.email})
    if not user:
        raise HTTPException(status_code=404)
    if user['password'] != signin.password:
        raise HTTPException(status_code=401)
    if user['is_activ'] == False:
        code_activation = str(random.randint(100000, 999999))
        db.users.update_one({'email':signin.email},{"$set":{"code_activation":code_activation}})
        await send_mes(signin.email, code_activation)
        raise HTTPException(status_code=426)
    access_token = await create_access_token({"email":signin.email})
    response.set_cookie(key="session_token", value=access_token)
    from models.user import User
    return User(email=signin.email,
                tel=user['tel'],
                session_token=access_token,
                name=user['name'],
                surname = user['surname'])

@router.post("/auth_signup")
async def Registration_User(signup:Signup):
    user = await db.users.find_one({'email': signup.email})
    if user:
        raise HTTPException(status_code=409)
    code_activation = str(random.randint(100000, 999999))
    await db.users.insert_one({"_id":str(uuid.uuid4()),
                               "name":signup.name,
                               "surname":signup.surname,
                               "email":signup.email,
                               "password":signup.password,
                               "tel":signup.tel,
                               "code_activation":code_activation,
                               "is_activ":False})
    await db.statistics.insert_one({"_id":str(uuid.uuid4()),
                                    "tel":signup.tel,
                                    "count":0})
    await send_mes(signup.email,code_activation)
    return signup

@router.post("/auth_activ_user")
async def activ_user(new_token:Activ_user):
    if await check_activ_user_form_emailhash(new_token.token):
        return True
    else:
        return False

@router.get("/auth_is_login")
async def is_login(request: Request):
    return await check_auth_ret_user(request)
    
@router.post("/patch_user")
async def patch_user(patch:patch_user,request: Request):
    user = await check_auth_user(request)
    await db.users.update_one({"_id":user['_id']},{"$set":{"name":patch.name,
                                                           "surname":patch.surname,
                                                           "email":patch.email,
                                                           "tel":patch.tel}})
    return patch

