from hashlib import new
import random
import re
from fastapi import APIRouter
from pydantic.networks import HttpUrl
from starlette.routing import request_response
from config import server
from config.mongodb import db
from fastapi import HTTPException
from starlette.requests import Request
from datetime import timedelta, datetime
from utils.email import send_mes
from models.services import *
from utils.authentication import check_auth_user,check_auth_moderator
import uuid
from static.services import Services_specialization
from static.Dictionary import city_type
from utils.filter import select_pages
from utils.services import get_lang_offerData
router = APIRouter(prefix=server.Server_config.prefix,
                   responses=server.Server_config.responses,
                   tags=['services'])
 
 

@router.get("/get_moder_services")
async def get_moder_services(request: Request):
    user = await check_auth_moderator(request)
    if user['type'] != 'services':
        raise HTTPException(status_code=409)
    try:
        list_services = []
        async for services  in db.services.find({'state':0}):
            list_img = [] 
            for img in services['offerData'].get("listPhotos"):
                list_img.append({"imgSrc":"https://maidon.tj/images_services/" + img.get('imgName')})
            services['offerData']['listPhotos'] = list_img
            list_services.append({"id":services['_id'],
                                "offerData":await get_lang_offerData(services['offerData']),
                                "storeService": services['storeService']})
        return list_services
    except:
        return HTTPException(status_code=409)

@router.post("/active_services")
async def acive_offer(services: Activ_services, request: Request):
    user = await check_auth_moderator(request)
    try:
        services_update = await db.services.find_one({"_id": services.id})
        if services_update:
            await db.services.update_one({"_id": services.id}, {"$set": {"state":services.state}})
            if services.note !="":
                chat = await db.moderator_chat.find_one({"id_user":services_update['id_user']})
                if chat:
                    text = f"В обьявлении {services_update['type']} ошибка: {services.note}"
                    db.moderator_chat.update_one({"_id":chat['_id']},{"$set":{"unread":services_update['id_user']}})

                    await db.moderator_chat.update_one({"_id":chat['_id']},
                                              {"$push":{"message":{"user":'moderator',
                                                                   "text":text,
                                                                   "date":datetime.now().strftime('%H:%M - %m.%d.%Y')}}})

        return
    except:
        return HTTPException(status_code=409)

@router.get("/get_services/{id}")
async def get_services(id:str):
    try:
        userdb = await db.users.find_one({"_id":id})
        if not userdb and userdb['account_type'] not in ['entity','individual']:
            raise HTTPException(status_code=404)
        value_review = 0.00
        if len(userdb['list_reviews']) !=0:
            for review in userdb['list_reviews']:
                value_review += review.get('value')
            value_review = round(float(value_review/len(userdb['list_reviews'])),2)
        
        user = {
            "_id":userdb['_id'],
            'account_type':userdb['account_type'],
            'tel':userdb['tel'],
            'workDate':userdb['workDate'],
            'specialization':userdb['specialization'],
            'about':userdb['about'],
            'website':userdb['website'],
            'avatar':userdb['avatar'],
            "review":value_review,
            "list_reviews":userdb['list_reviews']
        }
        
        if user['account_type'] == 'entity':
            user.update({"userInfo":userdb['companyName']})
        else:
            user.update({"userInfo":f'{userdb["surname"]} {userdb["name"]}'})
        
            
        if user['avatar'] != "": 
                user['avatar'] = "https://maidon.tj/avatar/" + user['avatar']
        if not user:
            raise HTTPException(status_code=404)
        list_services = []
        async for services in db.services.find({"id_user":user['_id']}): 
            services.pop("avatar")
            services.pop("userInfo")
            services.pop("account_type")
            services.pop("tel")
            services.pop("id_user")
            services.pop("about")
        #if services['state'] < 1:
        #    return HTTPException(status_code=404)
            list_img = []
            services['offerData'] = await get_lang_offerData(services['offerData'])
            for img in services['offerData'].get("listPhotos"):
                list_img.append("https://maidon.tj/images_services/" + img.get('imgName'))
            services['offerData']['listPhotos'] = list_img
            services['user_workDate'] = user['workDate']
            list_services.append(services)

        
        return {"user":user,"list_services":list_services}

    except:
        return HTTPException(status_code=409)

@router.get("/get_user_services")
async def get_user_services(request: Request):
    user = await check_auth_user(request)
    if user['account_type'] not in ['entity','individual']:
        raise HTTPException(status_code=409)
    try:
        list_services = []
        async for services in db.services.find({'id_user':user['_id']}):
            list_img = []
            for img in services['offerData'].get("listPhotos"):
                list_img.append({"imgSrc":"https://maidon.tj/images_services/" + img.get('imgName'),"imgName":img.get('imgName')})
            services['offerData']['listPhotos'] = list_img
            
            list_services.append({
                "id":services['_id'],
                "id_user": services['id_user'],
                "userInfo": services['userInfo'],
                "offerData":await get_lang_offerData(services['offerData']),
                "storeService": services['storeService'],
                "state": services['state'],
            })
        return list_services
    except:
        raise HTTPException(status_code=409)

@router.patch('/patch_services')
async def patch_services(services:Patch_services, request: Request):
    user = await check_auth_user(request)
    if user['account_type'] not in ['entity','individual']:
            raise HTTPException(status_code=409)
    try:
        list_Images = []
        for post in services.offerData.listPhotos:
            image = await db.temp_img.find_one({"name": post.get('imgName')})
            if image:
                db.temp_img.delete_one({"name": post.get('imgName')})
                list_Images.append({"imgName": image['newName']})
            else:
                list_Images.append({"imgName": post.get('imgName')})

        services.offerData.listPhotos = list_Images
        if services.id:
            patch_services = await db.services.find_one({"_id":services.id,"id_user":user['_id']})
            if not patch_services:
                raise HTTPException(status_code=404)
            await db.services.update_one({"_id":services.id},
                                        {"$set":{
                                                    "offerData": dict(services.offerData),
                                                    "storeService": services.storeService}
                                        })
            return services
        else:
            new_services ={"_id":str(uuid.uuid4()),
                        "id_user":user['_id'],
                        "userInfo":f'{user["surname"]} {user["name"]}',
                        "about":user['about'],
                        "avatar":user['avatar'],
                        "account_type":user['account_type'],
                        "offerData":dict(services.offerData),
                        "storeService":services.storeService,
                        "date": int(datetime.now().timestamp()),
                        'tel':user['tel'],
                        "state":0}
            db.services.insert_one(new_services)
            return services

    except:
        raise HTTPException(status_code=409)
      

@router.post("/delete_services")
async def delete_services(delete_services:Delete_services,request: Request):
    user = await check_auth_user(request)
    if user['account_type'] not in ['entity','individual']:
            raise HTTPException(status_code=409)
    try:
        services = await db.services.find_one({"_id":delete_services.id,"id_user":user['_id']})
        if services:
            db.services.delete_one({"_id":delete_services.id})
        else:
            return HTTPException(status_code=404)
    except:
        raise HTTPException(status_code=409)

@router.get("/list_services")
async def get_list_account_services(specialization:str = None,type:str = None,page: Optional[int] = 1):
    try:
        account_list = []
        request_response = {}
        if specialization:
            request_response.update({"offerData.specialization":specialization})
        if type:
            request_response.update({'account_type':type})
        pages = await select_pages(db.services,request_response)
      
        async for post in db.services.find(request_response).sort('date', -1).skip((page-1) * 20).limit(20):
            if len(post['storeService']) > 2:
                post['storeService_sum'] =  f'Всего услуг - {len(post["storeService"])}'
                post['storeService'] = post['storeService'][:2]
            if post['avatar'] != "": 
                post['avatar'] = "https://maidon.tj/avatar/" + post['avatar']
            list_img = []
            for img in post['offerData'].get("listPhotos"):
                list_img.append({"imgSrc":"https://maidon.tj/images_services/" + img.get('imgName'),"imgName":img.get('imgName')})
            post['offerData']['listPhotos'] = list_img  
            post['offerData'] = await get_lang_offerData(post['offerData'])
            account_list.append(dict(post))
        return {"account_list":account_list,"pages":pages}   
    except:
        raise HTTPException(status_code=409)


@router.get("/get_list_specialization")
async def get_list_specialization():
    return Services_specialization.value

@router.get("/get_list_city")
async def get_list_city():
    return city_type.options