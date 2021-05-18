from typing import List
from fastapi import APIRouter, WebSocket
from config import server
from models.chat import *
from config.mongodb import *
from starlette.requests import Request
from utils.authentication import *
from utils.ad import *

router = APIRouter(prefix=server.Server_config.prefix,
                   responses=server.Server_config.responses,
                   tags=['chat'])

@router.post("/open_chat")
async def get_id_chat(chat:Open_chat,request: Request):
    user = await check_auth_user(request)
    try:
       id_list = chat.id_offer.split("-")

       table = await select_table(id_list[1], id_list[0])
       offer = await table.find_one({"_id":chat.id_offer})

       if not offer:
           raise HTTPException(status_code=409)
       if user['_id'] == offer['id_user']:
           return Response(status_code=481)
       current_chat = await db.chat.find_one({"id_offer":chat.id_offer,"user.id":
                                             user['_id']})
     
       if current_chat:
           if user['_id'] == current_chat['user'][0].get('id') or user['_id'] == current_chat['user'][1].get('id'):
               return {"id_chat":current_chat['_id']}
           else:
               raise HTTPException(status_code=409)
       else:
           id_chat = str(uuid.uuid4())
           await db.chat.insert_one({"_id":id_chat,
                                     "title":offer['title'],
                                     "image":offer['offerPhothos'][0].get("imgName"),
                                     "id_offer":chat.id_offer,
                                     "unread":offer['userInfo'], 
                                     'user':[
                                             {"id":user['_id'],"name":f"{user['surname']} {user['name']}"},
                                              {"id":offer['id_user'],"name":offer['userInfo']}],
                                     "message":[]})
           return {"id_chat":id_chat}      
    except:
       raise HTTPException(status_code=409)

@router.post("/get_messages")
async def get_messages(chat:Get_messages,request: Request):
    user = await check_auth_user(request,1)
    try:
       current_chat = await db.chat.find_one({"_id":chat.id_chat})
       if current_chat:
           if user['_id'] == current_chat['user'][0].get('id') or user['_id'] == current_chat['user'][1].get('id'):
               list_messages = []
               if current_chat['unread'] == user['_id']:
                   await db.chat.update_one({"_id":chat.id_chat},{"$set":{"unread":""}})
               for mes in current_chat['message']:
                   who_send = "self"
                   if mes.get('user') != user['_id']:
                       who_send = "remote"
                   list_messages.append({"user":who_send,"text":mes.get('text'),'date':mes.get('date')})
               to_user = ""
               if current_chat['user'][0].get('id') != user['_id']:
                   to_user = current_chat['user'][0].get('name')
               else:
                   to_user = current_chat['user'][1].get('name')
               return {"messages":list_messages,
                       "title":current_chat['title'],
                       "image":"https://mirllex.site/img/" + current_chat['image'],
                       'user_name':to_user}
           else:
               raise HTTPException(status_code=409)
       current_chat = await db.moderator_chat.find_one({"_id":chat.id_chat})
       if current_chat:
           if user['_id'] == 'moderator':
              list_messages = []
              if current_chat['unread'] == user['_id'] or current_chat['complaint']:
                  await db.moderator_chat.update_one({"_id":chat.id_chat},{"$set":{"unread":"","complaint":False}})
              for mes in current_chat['message']:
                  who_send = "self"
                  if mes.get('user') != user['_id']:
                      who_send = "remote"
                  list_messages.append({"user":who_send,"text":mes.get('text'),'date':mes.get('date')})
              return {"messages":list_messages,
                       "title":f"Чат с {current_chat['user_info']}",
                       "image":"",
                       'user_name':current_chat['user_info']}
           else:
             if current_chat['id_user'] != user['_id']:
                 raise HTTPException(status_code=409)
             list_messages = []
             if current_chat['unread'] == user['_id']:
                  await db.moderator_chat.update_one({"_id":chat.id_chat},{"$set":{"unread":""}})
             for mes in current_chat['message']:
                  who_send = "self"
                  if mes.get('user') != user['_id']:
                      who_send = "remote"
                  list_messages.append({"user":who_send,"text":mes.get('text'),'date':mes.get('date')})
             return {"messages":list_messages,
                       "title":f"Чат поддержки",
                       "image":"",
                       'user_name':"Модератор"}



       else:
           return Response(status_code=404)
    except:
       raise HTTPException(status_code=409)


@router.get("/get_user_chats")
async def get_user_chats(request: Request):
    user = await check_auth_user(request,1)
    
    try:
       list_chats = []
       if user['_id'] == 'moderator':
           async for chat in db.moderator_chat.find():
               list_chats.append({"id":chat['_id'],
                              "title":f"Чат с {chat['user_info']}",
                              "unread":chat['unread'] == user['_id'] or chat['complaint'],
                              "image":"",
                              "user_name":chat['user_info']}) 
           return list_chats   
       moderator_chat = await db.moderator_chat.find_one({"id_user":user['_id']})
       if moderator_chat:
          list_chats.append({"id":moderator_chat['_id'],
                              "title":"Чат поддержки",
                              "unread":moderator_chat['unread'] == user['_id'],
                              "image":"",
                              "user_name":"Модератор"})
       async for chat in db.chat.find({"user":{"$elemMatch":{"id":user['_id']}}}):
           if len(chat['message']) > 0:
               to_user = ""
               if chat['user'][0].get('id') != user['_id']:
                   to_user = chat['user'][0].get('name')
               else:
                   to_user = chat['user'][1].get('name')
               list_chats.append({"id":chat['_id'],
                              "title":chat['title'],
                              "unread":chat['unread'] == user['_id'],
                              "image":"https://mirllex.site/img/" + chat['image'],"user_name":to_user})
           else:
               await db.chat.delete_one({"_id":chat['_id']})
       return list_chats 
    except:
       raise HTTPException(status_code=409)

@router.post("/delete_chat")
async def get_id_chat(chat:Get_messages,request: Request):
    user = await check_auth_user(request)
    try:
       current_chat = await db.chat.find_one({"_id":chat.id_chat})
       if not chat:
           return
       if user['_id'] == current_chat['user'][0].get('id') or user['_id'] == current_chat['user'][1].get('id'):
           await db.chat.delete_one({"_id":current_chat['_id']}) 
    except:
       raise HTTPException(status_code=409)
