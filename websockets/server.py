from fastapi import FastAPI, Response, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from config.mongodb import *
from utils.authentication import *
import datetime
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 

class ConnectionManager:
    def __init__(self):
        self.active_connections: List = []

    async def connect(self, websocket: WebSocket,token:str,chat:str, user:str):
        find = False
        print("lol")
        for connection in self.active_connections:
           if connection.get('chat') == chat:
               connection['connect'].append({"ws":websocket,"user":user})
               find = True
               print(self.active_connections)
               await websocket.accept()
               return
        if not find:
           self.active_connections.append({"chat":chat,
                                           "connect":[{"ws":websocket,
                                                       "user":user}]})
        print(self.active_connections)
        await websocket.accept()
      
        

    def disconnect(self, websocket: WebSocket,chat:str,user:str):
       for connection in self.active_connections:
           if connection.get('chat') == chat:
               for ws in connection.get('connect'):
                   if websocket == ws.get('ws'): 
                       connection['connect'].remove(ws) 
                       print("User close!")
                   if len(connection.get('connect')) == 0:
                       self.active_connections.remove(connection)
                       print("Session close!")
                       return
  
    async def broadcast(self,websocket: WebSocket, chat:str, message: str,user:str,another_user:str):
        for connection in self.active_connections:
            if connection.get('chat') == chat:
                unread = another_user
                for ws in connection.get('connect'):
                    who_sendmessage = "remote"
                    if ws.get('user') == user: 
                        who_sendmessage = "self"
                    else:
                        unread = ""
                    await ws.get('ws').send_text('{"user":"'+ who_sendmessage + '","text":"'+message+'", "date":"' + datetime.datetime.now().strftime('%H:%M - %m.%d.%Y') + '"}')
                await db.chat.update_one({"_id":chat},{"$push":{"message":{"user":user, 
                                                                               "text":message,
                                                                               "date":datetime.datetime.now().strftime('%H:%M - %m.%d.%Y')}}})
                if unread!= "":
                    await db.chat.update_one({"_id":chat},{"$set":{"unread":unread}})


  
manager = ConnectionManager()
 
@app.websocket("/send_message/{token}/{chat_id}")
async def websocket_endpoint(websocket: WebSocket,token:str,chat_id:str):
    try:
        user = await get_current_session_user(token)
        print(user)
        current_chat = await db.chat.find_one({'_id':chat_id})
        if not current_chat:
            return 

        if user['_id'] == current_chat['user'][0].get('id'):
            another_user = current_chat['user'][1].get('id')
        else: 
            another_user = current_chat['user'][0].get('id')

        if user['_id'] != current_chat['user'][0].get('id') and user['_id'] != current_chat['user'][1].get('id'):
            return 
        print(manager.active_connections)
        await manager.connect(websocket,token,chat_id,user['_id'])
        print(manager.active_connections)
        while True:        
            data = await websocket.receive_text()
            data = data.replace('\n',"")
            if data == "bdb86498-3d50-430e-b566-7a95345c7712":
                manager.disconnect(websocket,chat_id,user['_id'])
                return

            await manager.broadcast(websocket,chat_id,data,user['_id'],another_user)
    except:
        manager.disconnect(websocket,chat_id,user['_id'])

 
    
       