import uuid
from fastapi import APIRouter
from config import server
from models.authentication import *
from models.account import *
from config.mongodb import *
from utils.authentication import *
from utils.email import send_mes,send_mes_reset_pass
from utils.filter import *


router = APIRouter(prefix=server.Server_config.prefix,
                   responses=server.Server_config.responses,
                   tags=['account'])

@router.post("/get_accounts")
async def get_account(account:Account):
    #try:
        print(account)
        if account.type not in ['realtor','agency']:
            raise HTTPException(status_code=409)
        list_accounts = []
        async for user in db.users.find({"account_type":account.type}).skip((account.page-1) * 10).limit(10):
            item = {"id":user['_id'],"offer_count":user['offer_count']}
            value_review = 0.00
            for review in user['list_reviews']:
                value_review += review.get('value')
            if len(user['list_reviews']) !=0:
                value_review = round(float(value_review/len(user['list_reviews'])),2)

            if user['avatar'] !="":
                user['avatar'] = "https://mirllex.site/avatar/" + user['avatar']
            review_text = ""
            review_last = {}
            review_lastuser =""    
  
 
            if len(user['list_reviews']) > 0:
               review_last = user['list_reviews'][len(user['list_reviews'])-1]
               review_text = review_last.get('text') 
               review_lastuser = review_last.get('user')
        
            item = {"id":user['_id'],
                    "offer_count":user['offer_count'],
                    "avatar":user['avatar'],
                    "review":value_review,
                    "review_lastuser":review_lastuser,   
                    "review_text":review_text,
                    "count_reviews":len(user['list_reviews'])}
            if account.type == 'agency':
                 item.update({"name":user['companyName']})
            else:
                 item.update({"name":f"{user['surname']} {user['name']}"})
            
            list_accounts.append(item)
 
        pages = await db.users.count_documents({"account_type":account.type})
        if pages % 10 == 0:
           pages = pages // 10
        else:
            pages = pages // 10 + 1
        return {"count":len(list_accounts),"accounts":list_accounts,"pages":pages}
    #except:
        raise HTTPException(status_code=409)

@router.post("/add_review")
async def add_review(review:Review,request: Request):
    user = await check_auth_user(request)
    try:
        if user['_id'] == review.id:
            raise HTTPException(status_code=409)
        if user['account_type'] != "owner":
            raise HTTPException(status_code=409)
        review_user = await db.users.find_one({"_id":review.id})
        if review_user:
            db.users.update_one({"_id":review.id},
                                {"$push":{"list_reviews":{"user":f"{user['surname']} {user['name']}",
                                                         "text":review.text,
                                                         'date':datetime.datetime.now().strftime('%H:%M - %m.%d.%Y'),
                                                         "value":review.value}}})
        return
    except:
        raise HTTPException(status_code=409)


@router.get("/get_info_account/{id}")
async def get_info_account(id:str):
    try:
        user = await db.users.find_one({"_id":id})
        if not user:
            return Response(status_code=409)
        list_offers = []
        for table in list_db:
            async for offer in table.find({"id_user":user['_id']}):
                object = offer['offer_object'].get('object')
                if offer['offer_object'].get('object') == 'office':
                    object = "commercy"
                deal = "buy"
                if offer['offer_price'].get('deal') == "rent_long":
                    deal = "rent"
                if offer['offer_price'].get('deal') == "rent_day":
                    deal = "daily"
                offer = await get_offer(offer)

                offer.update({"object":object,"deal":deal})
                list_offers.append(offer)
        user['list_offers'] = list_offers
        user.pop('account_type')
        user.pop('password')
        user.pop('is_activ')
        user.pop('offer_count')
        user.pop('_id')
        if user['avatar'] !="":
           user['avatar'] = "https://mirllex.site/avatar/" + user['avatar']
        for key in list(user.keys()):
            if user.get(key) == "" and key != 'avatar':
               user.pop(key) 
        value_review = 0.00
        for review in user['list_reviews']:
            value_review += review.get('value')
        if len(user['list_reviews']) !=0:
            value_review = round(float(value_review/len(user['list_reviews'])),2)
        user['review'] = value_review
        return user 
    except:
        raise HTTPException(status_code=409)


