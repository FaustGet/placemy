import random
import uuid
from starlette.requests import Request
from fastapi import APIRouter, HTTPException

from config import server
from config.mongodb import db
from models.Ad import Place_an_ad
from utils.ad import *
from utils.authentication import  check_auth_user


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
    await push_offerdb(new_ad.offerType.get("estate"),advertisement)
    return advertisement