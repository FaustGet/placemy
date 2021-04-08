import os
import shutil
import datetime
from config import server
from fastapi import APIRouter, UploadFile, File
from models.files import*
from config.mongodb import db

router = APIRouter(prefix=server.Server_config.prefix,
                   responses = server.Server_config.responses,
                   tags=['files'])

@router.post("/offer_uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
      with open('/app/images/' + file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
      date = datetime.datetime.now()
      await db.temp_img.insert_one({"name":file.filename,
                                    "date":int(date.timestamp())})
    finally:
      file.file.close()
    return 




