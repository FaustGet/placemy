import os
import shutil
import datetime
from config import server
from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.requests import Request
from config.mongodb import db, list_db
import random
from utils.authentication import check_auth_user

router = APIRouter(prefix=server.Server_config.prefix,
                   responses=server.Server_config.responses,
                   tags=['files'])


@router.post("/offer_uploadfile")
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    user = await check_auth_user(request)
    try:
        oldName = file.filename
        date = datetime.datetime.now() + datetime.timedelta(seconds=3600)
        file.filename = str(int(date.timestamp())) + str(random.randint(100, 999)) + ".jpg"
        with open('/app/images/' + file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        await db.temp_img.delete_one({"newName": file.filename})
        await db.temp_img.insert_one({"name": oldName, "newName": file.filename,
                                      "date": int(date.timestamp())})
        return
    except:
        raise HTTPException(status_code=409)


@router.post("/upload_avatar")
async def upload_avatar(request: Request, file: UploadFile = File(...)):
    user = await check_auth_user(request)
    try:
        date = datetime.datetime.now()
        file.filename = str(int(date.timestamp())) + str(random.randint(100, 999)) + ".jpg"
        with open('/app/avatar/' + file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        if user['avatar'] != "":
            with open('/app/avatar/' + user['avatar'], "wb") as buffer:
                os.remove(buffer.name)
        await db.users.update_one({"_id": user['_id']}, {"$set": {"avatar": file.filename}})
        for table in list_db:
            await table.update_many({"id_user": user['_id']}, {"$set": {"user_avatar": file.filename}})
        return {"avatar": "https://mirllex.site/avatar/" + file.filename}
    except:
        raise HTTPException(status_code=409)
    


@router.delete("/delete_avatar")
async def delete_avatar(request: Request):
    user = await check_auth_user(request)
    try:
        with open('/app/avatar/' + user['avatar'], "wb") as buffer:
            os.remove(buffer.name)
        await db.users.update_one({"_id": user['_id']}, {"$set": {"avatar": ""}})
        for table in list_db:
            await table.update_many({"id_user": user['_id']}, {"$set": {"user_avatar": ""}})
        return
    except:
        return

