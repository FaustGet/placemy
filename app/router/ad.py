import datetime
import random
import uuid
from typing import Optional

from starlette.requests import Request
from fastapi import APIRouter, HTTPException

from config import server
from config.mongodb import db
from models.Ad import Place_an_ad
from models.filters import *
from utils.ad import *
from utils.authentication import  check_auth_user
from utils.filter import *

router = APIRouter(prefix=server.Server_config.prefix,
                   responses = server.Server_config.responses,
                   tags=['ad'])

@router.post("/offer_place_an_ad")
async def Place_an_ad(new_ad:Place_an_ad,request: Request):
    #user = await check_auth_user(request)
    id = str(uuid.uuid4())
    advertisement = {"_id": id,
                    "id_user": "123",
                    "map_address": new_ad.offerMap.get('map_address'),
                    "map_marker": new_ad.offerMap.get('map_marker')}

    offer_object = await get_offer_object(new_ad.offerType.get("object_living"),
                                    new_ad.offerType.get("object_commercy"),
                                    new_ad.offerObject)
    offer_price = await get_offer_price(new_ad.offerType.get('deal'),new_ad.offerPrice)
    if new_ad.offerType.get('account') == 'agent':
        offer_price.update({"percentageTransaction":
                                new_ad.offerPrice.get("inputs").get('percentageTransaction').get('value')})
    advertisement.update({"offer_object": offer_object})
    advertisement.update({"offer_price": offer_price})
    advertisement.update({"offerDescription": new_ad.offerDescription})
    advertisement.update({"offerPhothos": new_ad.offerPhothos})
    await push_offerdb(new_ad.offerType.get("estate"),advertisement)
    for post in new_ad.offerPhothos:
        db.temp_img.delete_one({"name":post.get('imgName')})
    return advertisement

@router.delete("/delete_offer")
async def delete_offer(id:str, request:Request):
    user = await check_auth_user(request)
    offer = await get_offer(id)
    if offer['id_user'] == user['_id']:
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

@router.get("/offer/{id}")
async def get_offer_on_id(id:str):
    offer = await get_offer(id)
    return offer


@router.get("/get_sales_offers")
async def get_offer_on_object(deal: Optional[str] = "",
                              kind: Optional[str] = "",
                              type: Optional[str] = "",
                              object: Optional[str] = "",
                              repair: Optional[str] = "",
                              pagina: Optional[int] = 0):
    table = await select_table(deal, kind)
    if table == -1:
        return []
    list_offer = await select_offers(kind,type,object,repair,pagina,table)
    return list_offer

@router.post("/get_filter_offers")
async def get_filter_offers(filter_offers:Filter_offers):
    print(filter_offers)
    return