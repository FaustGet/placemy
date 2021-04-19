import os
import shutil
import datetime
from config import server
from fastapi import APIRouter, UploadFile, File
from models.files import*
from config.mongodb import db
import random

router = APIRouter(prefix=server.Server_config.prefix,
                   responses = server.Server_config.responses,
                   tags=['files'])

@router.post("/offer_uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
      oldName = file.filename
      date = datetime.datetime.now() + datetime.timedelta(seconds=3600)
      file.filename = str(int(date.timestamp())) + str(random.randint(100, 999)) + "-1.jpg"
      with open('/app/images/' + file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
      await db.temp_img.delete_one({"newName":file.filename})
      await db.temp_img.insert_one({"name":oldName,"newName":file.filename,
                                    "date":int(date.timestamp())})
    finally:
      file.file.close()
    return 

