import random
import uuid
import datetime
from starlette.requests import Request
from fastapi import APIRouter, HTTPException
from config import server
from config.mongodb import db
from models.Ad import Place_an_ad
from utils.ad import *
from utils.authentication import *
from typing import Optional
from models.filters import *
from utils.filter import *
from utils.files import change_images
from static.Dictionary import office_type, ground_type,city_type

router = APIRouter(prefix=server.Server_config.prefix,
                   responses = server.Server_config.responses,
                   tags=['ad'])

#ыфвыфв

@router.post("/offer_place_an_ad")
async def Place_an_ad(new_ad:Place_an_ad,request: Request):
    user = await check_auth_user(request)
    try:
        advertisement = {"id_user": user['_id'],
                         "userInfo":user['surname'] +" " + user['name'],
                         "tel":user['tel'],
                        "map_address": new_ad.offerMap.get('map_address'),
                        "map_marker": new_ad.offerMap.get('map_marker')}

        offer_object = await get_offer_object(new_ad.offerType.get("object_living"),
                                        new_ad.offerType.get("object_commercy"),
                                        new_ad.offerObject)
        offer_price = await get_offer_price(new_ad.offerType.get('deal'),new_ad.offerPrice)
        offer_object.update({'city':new_ad.offerObject.get('selects').get('cities').get('value')})
        if new_ad.offerType.get('account') == 'agent':
            offer_price.update({"percentageTransaction":
                                    new_ad.offerPrice.get("inputs").get('percentageTransaction').get('value')})
        title = await get_title(offer_object)
        advertisement.update({'title':title})
        advertisement.update({"offer_object": offer_object})
        advertisement.update({"offer_price": offer_price})
        
        advertisement.update({"offerDescription": new_ad.offerDescription})
        offerChangePhotos =  await change_images(new_ad.offerPhothos)
        advertisement.update({"date": int(datetime.datetime.now().timestamp())})
        list_offerImages = []
        for post in new_ad.offerPhothos:
            image = await db.temp_img.find_one({"name":post.get('imgName')})
            if image:  
                list_offerImages.append({"imgName":image['newName']})
                db.temp_img.delete_one({"name":post.get('imgName')})
        print(list_offerImages)
        advertisement.update({"offerPhothos": list_offerImages})
        await push_offerdb(new_ad.offerType.get("estate"),advertisement)
        return
    except:
        raise HTTPException(status_code=409)
 
@router.get("/offer/{id}")
async def get_offerID(id:str):
    offer = await get_offer_on_id(id)
    return offer

@router.delete("/delete_offer")
async def delete_offer(id:str, request:Request):
    user = await check_auth_ret_user(request)
    if user == -1:
        return ""
    offer = await get_offer(id)
    if offer == "":
        return offer
    if str(offer['id_user']) == str(user['_id']):
        id_list = id.split("-")
        estate = id_list[0]
        deal = id_list[1]
        if estate == "living":
            if deal == "sell":
                await db.sell_living.delete_one({"_id": id})
            if deal == "rent_long":
                await db.rent_long_living.delete_one({"_id": id})
            if deal == "rent_day":
                await db.rent_day_living.delete_one({"_id": id})
        if estate == "commercy":
            if deal == "sell":
                await db.sell_commercy.delete_one({"_id": id})
            if deal == "rent_long":
                await db.rent_long_commercy.delete_one({"_id": id})
            if deal == "rent_day":
                await db.rent_day_commercy.delete_one({"_id": id})

@router.get("/get_sales_offers")
async def get_offer_on_object(deal: Optional[str] = "",
                              kind: Optional[str] = "",
                              type: Optional[str] = "",
                              object: Optional[str]="",
                              repair: Optional[str]="",
                              page: Optional[int]=1):
    table = await select_table(deal, kind)
    if table == -1:
        return []
    list_offer = await select_offers(kind,type,object,repair,pagina,table)
    return list_offer 


@router.post("/get_filter_offers")
async def get_filter_offers(filter_offers:Filter_offers):
    print(filter_offers)
    table = await select_table(filter_offers.deals.get('value'),filter_offers.objects.get('value')) 
    if table == -1:
        return []
    list_offer = await select_filter_offers(filter_offers, table,filter_offers.page)
    return list_offer

