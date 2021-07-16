import uuid
from fastapi import APIRouter
from config import server
from models.authentication import *
from models.user import *
from config.mongodb import *
from utils.authentication import *
from utils.email import send_mes
from utils.filter import *
from datetime import datetime

router = APIRouter(prefix=server.Server_config.prefix,
                   responses=server.Server_config.responses,
                   tags=['authentication'])


@router.post("/signin")
async def login(signin: Signin, response: Response):
    user = await db.users.find_one({'tel': signin.tel})
    if not user:
        user = await db.moderators.find_one({'tel': signin.tel})
       
        if not user: 
            raise HTTPException(status_code=404)
        else:
            user['is_moder'] = True
            
    else:
        user['is_moder'] = False
    if user['password'] != signin.password:
        raise HTTPException(status_code=401)
    if user['is_activ'] == False:
        code_activation = str(random.randint(100000, 999999))
        db.users.update_one({'tel': signin.tel}, {"$set": {"code_activation": code_activation}})
        await send_mes(signin.tel, code_activation)
        raise HTTPException(status_code=426)
    access_token = await create_access_token({"tel": signin.tel})
    response.set_cookie(key="session_token", value=access_token)
    if user['avatar'] != "":
        user['avatar'] = "https://maidon.tj/avatar/" + user['avatar']
    user_view = await db.statistics.find_one({"tel":user['tel']})
    user.pop('is_activ')
    user['session_token'] = access_token
    return user

 
@router.post("/signup")
async def Registration_User(signup: Signup):
    try:    
        user = await db.users.find_one({'tel': signup.tel})
        if user:
            raise HTTPException(status_code=409)
        code_activation = str(random.randint(100000, 999999))
        user_model = dict(signup)
        id_user = str(uuid.uuid4())
        user_model['_id'] = id_user
        user_model['is_activ'] = False
        user_model['avatar'] = ""
        user_model['offer_count'] = 0
        user_model['list_reviews'] = []
        user_model['code_activation'] = code_activation
        user_model['date'] = datetime.now() + timedelta(hours=24)
        await db.users.insert_one(user_model)
        user_info = f'{signup.surname} {signup.name}'
        print(user_model['account_type'])
        print(user_model['companyName'])
        if user_model['account_type'] in ['agency','entity']:
            user_info = user_model['companyName']
        await db.moderator_chat.insert_one({"_id":str(uuid.uuid4()),
                                            "unread":"", 
                                            "id_user":id_user,
                                            'user_info':user_info,
                                            "message":[],
                                            "complaint":False})
        await send_mes(signup.tel, code_activation)
        return signup
    except: 
        raise HTTPException(status_code=409)



@router.post("/send_activate_code")
async def send_activate_code(activ_user: Activ_user):
    user = await db.users.find_one({"tel":activ_user.tel,"code_activation":activ_user.code})
    if user:
        db.users.update_one({"tel":activ_user.tel},{"$set":{"is_activ":True,"code_activation":""}})
        return True
    else:
        return False


@router.get("/check_access")
async def check_access(request: Request):
    return await check_auth_ret_user(request)


@router.post("/patch_info")
async def patch_user_info(patch: patch_user, request: Request):
    user = await check_auth_user(request)
    try:
        print(user['account_type'])
        if user['account_type'] in ['agency','entity']:
            print(patch.companyName)
            request_json_moder = {"$set":{"user_info":patch.companyName}}
            request_json_chat = {"$set":{"user.$.name":patch.companyName}}
            request_json = {"$set":{"tel":patch.tel,'userInfo': patch.companyName}}
        if user['account_type'] in ['realtor','owner','individual']:
            request_json_moder = {"$set":{"user_info":f"{patch.surname} {patch.name}"}}
            request_json_chat = {"$set":{"user.$.name":f"{patch.surname} {patch.name}"}}
            request_json = {"$set":{"tel":patch.tel,'userInfo': f"{patch.surname} {patch.name}"}}
 
        if user['account_type'] in ['individual']:
            request_json_moder = {"$set":{"user_info":f"{patch.surname} {patch.name}"}}
            request_json_chat = {"$set":{"user.$.name":f"{patch.surname} {patch.name}"}}
            request_json = {"$set":{"tel":patch.tel,'userInfo': f"{patch.surname} {patch.name}"}}
        await db.moderator_chat.update_one({'id_user':user['_id']},request_json_moder)

        await db.chat.update_many({"user":{"$elemMatch":{"id":user['_id']}}},request_json_chat)
        if user['account_type'] in ['realtor','owner','agency']:
            for table in list_db:
                await table.update_many({"id_user":user['_id']},request_json)
        if user['account_type'] in ['entity','individual']:
            await db.services.update_many({"id_user":user['_id']},request_json)
        await db.users.update_one({"_id": user['_id']}, {"$set": {"name": patch.name,
                                                                  "surname": patch.surname,
                                                                  "tel": patch.tel,
                                                                  "companyName": patch.companyName,
                                                                  "workDate":patch.workDate,
                                                                  "specialization":patch.specialization,
                                                                  "about":patch.about,
                                                                  "website":patch.website}})
        user = await db.users.find_one({"_id":user['_id']})
        if user['avatar'] != "": 
            user['avatar'] = "https://maidon.tj/avatar/" + user['avatar']
        return dict(user)
    except:
        raise HTTPException(status_code=409)


@router.post("/view_tel")
async def view_tel(view_offer:view_tel):
    try:
        id_list = view_offer.id.split("-")
        estate = id_list[0]
        deal = id_list[1]
        table = await select_table(deal, estate)

        offer = await table.find_one({'_id':view_offer.id})
        if offer:
            offer['view_tel'] = offer['view_tel'] + 1
            table.update_one({"_id":view_offer.id},{'$set':{'view_tel':offer['view_tel']}})
            return offer['view_tel']
        else:
            raise HTTPException(status_code=409)
    except:
        raise HTTPException(status_code=409)




@router.post("/patch_pass")
async def patch_user(patch: patch_user_password, request: Request):
    user = await check_auth_user(request)
    try:
        if user['password'] == patch.old_password:
            await db.users.update_one({"_id": user['_id']}, {"$set": {"password": patch.new_password}})
            return
        else:
            raise HTTPException(status_code=409)
    except:
        raise HTTPException(status_code=409)


@router.post("/reset_pass")
async def reset_pass(reset_pass:Reset_pass):
    try:      
        user = await db.users.find_one({'tel':reset_pass.tel})
        if not user:
            raise HTTPException(status_code=409)
        code_activation = str(random.randint(100000, 999999))
        db.users.update_one({'tel': reset_pass.tel}, {"$set": {"code_activation": code_activation}})
        await send_mes(reset_pass.tel, code_activation)            
        return 
    except:
        raise HTTPException(status_code=409)


@router.post("/restore_pass")
async def restore_password(restore_pass: Restore_pass):
    try:
        user = await db.users.find_one({"tel":restore_pass.tel,"code_activation":restore_pass.code})
        if user: 
            db.users.update_one({"tel":restore_pass.tel},{"$set":{"password":restore_pass.password,
                                 "code_activation":"","is_activ":True}})
            return True
        else:
            return False
    except:
        raise HTTPException(status_code=409)

@router.post("/add_complaint")
async def add_complaint(complaint:Complaint):
    try:
      user = await db.users.find_one({"_id":complaint.id_user})
      if not user:
         return Response(status_code=404)
      text = f"На обьявление '{complaint.title}' была подана следюущая жалоба:\n\n{complaint.text}\n"
          
      await db.moderator_chat.update_one({"id_user":complaint.id_user},
                                         {"$push":{"message":{"user":"moderator",                                              
                                                              "text":text,
                                                              "date":datetime.datetime.now().strftime('%H:%M - %m.%d.%Y')}}})
      await db.moderator_chat.update_one({"id_user":complaint.id_user},{"$set":{"unread":user['_id'],"complaint":True}})

      return
    except:
        raise HTTPException(status_code=409)