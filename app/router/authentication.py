import uuid
from fastapi import APIRouter
from config import server
from models.authentication import *
from models.user import *
from config.mongodb import *
from utils.authentication import *
from utils.email import send_mes,send_mes_reset_pass
from utils.filter import *
router = APIRouter(prefix=server.Server_config.prefix,
                   responses=server.Server_config.responses,
                   tags=['authentication'])


@router.post("/signin")
async def login(signin: Signin, response: Response):
    user = await db.users.find_one({'email': signin.email})
    if not user:
        user = await db.moderators.find_one({'email': signin.email})
        if not user: 
            raise HTTPException(status_code=404)
    if user['password'] != signin.password:
        raise HTTPException(status_code=401)
    if user['is_activ'] == False:
        code_activation = str(random.randint(100000, 999999))
        db.users.update_one({'email': signin.email}, {"$set": {"code_activation": code_activation}})
        await send_mes(signin.email, code_activation)
        raise HTTPException(status_code=426)
    access_token = await create_access_token({"email": signin.email})
    response.set_cookie(key="session_token", value=access_token)
    from models.user import User
    if user['avatar'] != "":
        user['avatar'] = "https://mirllex.site/avatar/" + user['avatar']
    user_view = await db.statistics.find_one({"tel":user['tel']})
    view = 0
    if not user_view:
         await db.statistics.insert_one({"_id": str(uuid.uuid4()),
                                    "tel": user['tel'],
                                    "view": 0})
    else:
      view = user_view['view']
    return User(tel=user['tel'],
                name=user['name'],
                surname=user['surname'],
                avatar=user['avatar'],
                session_token=access_token,
                view=view,
                is_moder=user['_id'] in Moderotor.id)


@router.post("/signup")
async def Registration_User(signup: Signup):
    try:
        user = await db.users.find_one({'email': signup.email})
        if user:
            raise HTTPException(status_code=409)
        code_activation = str(random.randint(100000, 999999))
        await db.users.insert_one({"_id": str(uuid.uuid4()),
                              "name": signup.name,
                               "surname": signup.surname,
                               "email": signup.email,
                               "password": signup.password,
                               "tel": signup.tel,
                               "code_activation": code_activation,
                               "avatar": "",
                               "is_activ": False})
        await db.statistics.insert_one({"_id": str(uuid.uuid4()),
                                    "tel": signup.tel,
                                    "view": 0})
        await send_mes(signup.email, code_activation)
        return signup
    except:
        raise HTTPException(status_code=409)



@router.post("/send_activate_code")
async def send_activate_code(new_token: Activ_user):
    if await check_activ_user_form_emailhash(new_token.token):
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
        if user['tel'] != patch.tel or user['name'] != patch.name or user['surname'] != patch.surname:
            for table in list_db:
                await table.update_many({"id_user":user['_id']},{"$set":{"tel":patch.tel,'userInfo': f"{patch.surname} {patch.name}"}})
            await db.statistics.update_one({"tel":user['tel']},{'$set':{'tel':patch.tel}})
        await db.users.update_one({"_id": user['_id']}, {"$set": {"name": patch.name,
                                                              "surname": patch.surname,
                                                              "tel": patch.tel}})
        await db.chat.update_many({"user":{"$elemMatch":{"id":user['_id']}}},
                                   {"$set":{"user.$.name":f"{patch.surname} {patch.name}"}})
        return patch
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
        print(reset_pass)
        user = await db.users.find_one({'email':reset_pass.email})
        print(user)
        if not user:
            raise HTTPException(status_code=409)
        if user['is_activ'] == False:
            code_activation = str(random.randint(100000, 999999))
            db.users.update_one({'email': reset_pass.email}, {"$set": {"code_activation": code_activation}})
            await send_mes(reset_pass.email, code_activation)
            return Response(status_code=426)
        else:
            code_activation = str(random.randint(100000, 999999))
            db.users.update_one({'email': reset_pass.email}, {"$set": {"code_activation": code_activation}})
            await send_mes_reset_pass(reset_pass.email, code_activation)            
        return 
    except:
        raise HTTPException(status_code=409)


@router.post("/restore_pass")
async def restore_password(new_token: Restore_pass):
    try:
        print(new_token)
        if await check_activ_user_form_emailhash(new_token.token,new_token.password):
            return True
        else:
            return False
    except:
        raise HTTPException(status_code=409)
