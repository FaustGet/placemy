import datetime

from config.mongodb import db
from utils.object_commercy import *
from utils.object_living import *
from utils.price__type import *

async def select_table(deal:str, kind:str):
    if kind == "commercy":
        if deal == "buy":
            return db.sell_commercy
        # if "deal" == "buy":
        #     return db.sell_commercy
        # if "deal" == "buy":
        #     return db.sell_commercy
    if deal == "buy":
        return db.sell_living
    # if deal == "buy":
    #     return db.sell_living
    # if deal == "buy":
    #     return db.sell_living
    return -1

async def select_count_rooms(request_json:dict,object:str):
    if object == "oneroom":
        request_json.update({"offer_object.count_rooms":1})
    if object == "tworoom":
        request_json.update({"offer_object.count_rooms": 2})
    if object == "threeroom":
        request_json.update({"offer_object.count_rooms": 3})
    if object == "fourroomormore":
        request_json.update({"offer_object.count_rooms": {"$gte":4}})
    return request_json

async def select_kind(kind:str,type:str,repair:str):
    if kind == "apartment":
        if repair != 'undefined':
            return {"offer_object.building_renovation":repair, "offer_object.object": kind}
        return {'offer_object.building_type': type,"offer_object.object": kind}
    return {"offer_object.object": kind}


async def select_offers(kind:str,type:str,object:str,repair:str,pagina:int,table):
    if kind == "commercy":
        list_offers = []
        async for post in table.find({"offer_object.office_type":object}).sort('date',-1):
            post['date'] = datetime.datetime.fromtimestamp(post['date']).strftime("%d.%m.%Y %H:%M")
            list_offers.append(post)
        return list_offers
    request_json = await select_kind(kind,type,repair)
    request_json = await select_count_rooms(request_json, object)
    list_offers = []
    async for post in table.find(request_json).sort('date', -1):
        post['date'] = datetime.datetime.fromtimestamp(post['date']).strftime("%d.%m.%Y %H:%M")
        list_offers.append(post)
    return list_offers

