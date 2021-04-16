import datetime

from config.mongodb import db
from models.filters import Filter_offers
from utils.object_commercy import *
from utils.object_living import *
from utils.price__type import *

async def select_table(deal:str, kind:str):
    if kind == "commercy" or kind == 'building':
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
    if not object:
        return request_json
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
    if kind == 'commercy':
        request_json = {"offer_object.object": 'office'}
    else:
        request_json = {"offer_object.object": kind}
    if (kind == "apartment") or (kind == "room") or (kind=='house'):
        if (repair != 'undefined') and (repair):
            request_json.update({"offer_object.building_renovation":repair})
        if (type) and (type!= 'allTypes'):
            request_json.update({'offer_object.building_type': type})
    return request_json

async def select_size(kind:str,sizeFrom:int,sizeTo:int,request_json:dict):
    if sizeTo == 0 and sizeFrom == 0:
        return request_json
    if kind == 'apartment' or kind == 'commercy':
        request_json.update({'offer_object.area':{'$gte':sizeFrom, '$lte':sizeTo}})
    if kind == 'room':
        request_json.update({'offer_object.area_room': {'$gte': sizeFrom, '$lte': sizeTo}})
    if kind == 'ground':
        request_json.update({'offer_object.area_land': {'$gte': sizeFrom, '$lte': sizeTo}})
    if kind == 'house':
        request_json.update({'offer_object.area_house': {'$gte': sizeFrom, '$lte': sizeTo}})
    if kind == 'building':
        request_json.update({'offer_object.area_building': {'$gte': sizeFrom, '$lte': sizeTo}})
    return request_json

async def select_commercy(typeCommercy:str,request_json:dict):
    if not typeCommercy:
        return request_json
    request_json.update({'offer_object.office_type':typeCommercy})
    return request_json

async def select_ground(kind:str,type:int,request_json:dict):
    if kind != 'house' and kind != 'ground':
        return request_json
    if type:
        request_json.update({'offer_object.ground_type':type})
    return request_json

async def select_price(deal:str,priceFrom:int,priceTo:int,request_json:dict):
    if priceTo == 0 and priceFrom == 0:
        return request_json
    if deal == 'buy':
        request_json.update({'offer_price.price':{'$gte': priceFrom, '$lte': priceTo}})
    return request_json

async def select_offers(kind:str,type:str,object:str,repair:str,pagina:int,table):
    list_offers = []
    if kind == "commercy":
        async for post in table.find({"offer_object.office_type":object}).sort('date',-1):
            post['date'] = datetime.datetime.fromtimestamp(post['date']).strftime("%d.%m.%Y %H:%M")
            list_offers.append(post)
        return list_offers
    request_json = await select_kind(kind,type,repair)
    request_json = await select_count_rooms(request_json, object)
    async for post in table.find(request_json).sort('date', -1).skip(pagina * 25):
        post['date'] = datetime.datetime.fromtimestamp(post['date']).strftime("%d.%m.%Y %H:%M")
        list_offers.append(post)
    return list_offers


async def select_filter_offers(filter_offers:Filter_offers,table):
    request_json = await select_kind(filter_offers.objects.get('value'),
                                     filter_offers.typeBuilding.get('value'),
                                     filter_offers.repair.get('value'))

    if filter_offers.objects.get('value') == "apartment":
        request_json = await select_count_rooms(request_json,filter_offers.rooms.get('value'))
    if filter_offers.address != '':
        request_json.update({'map_address':filter_offers.address})
    request_json = await select_size(filter_offers.objects.get('value'),
                                      filter_offers.sizeFrom,filter_offers.sizeTo,
                                      request_json)
    request_json = await select_price(filter_offers.deals.get('value'),
                                      filter_offers.priceFrom,filter_offers.priceTo,
                                      request_json)
    request_json = await select_ground(filter_offers.objects.get('value'),
                                       filter_offers.typeGround.get('value'),
                                       request_json)
    request_json =await select_commercy(filter_offers.typeCommercy.get('value'),request_json)
    list_offers = []
    print(request_json)
    async for post in table.find(request_json).sort('date', -1).skip(0 * 25):
        post['date'] = datetime.datetime.fromtimestamp(post['date']).strftime("%d.%m.%Y %H:%M")
        list_offers.append(post)
    print(list_offers)
    return list_offers


