import datetime

from config.mongodb import db
from utils.object_commercy import *
from utils.object_living import *
from utils.price__type import *
from models.filters import Filter_offers,List_filter_offers

async def select_table(deal:str, kind:str):

    if kind == "commercy" or kind == 'building':
        if deal == "buy" or deal == "sell":
            return db.sell_commercy
        if deal == "daily" or deal == "rent_day":
            return db.rent_day_commercy
        if deal == "rent" or deal == "rent_long":
            return db.rent_long_commercy 
    if deal == "buy" or deal == "sell":
        return db.sell_living
    if deal == "daily" or deal == "rent_day":
        return db.rent_day_living
    if deal == "rent" or deal == "rent_long":
        return db.rent_long_living 
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

async def select_price(deal:str,priceFrom:int,priceTo:int,request_json:dict):
    if priceTo == 0 and priceFrom == 0:
        return request_json
    if priceTo == 0:
        json = {'$gte': priceFrom}
    else:
        json = {'$gte': priceFrom, '$lte': priceTo}
    if deal == 'buy':
        request_json.update({'offer_price.price':json})

    if deal == 'rent_long' or deal == 'rent':
        request_json.update({'offer_price.price_mounth':json})

    if deal == 'rent_day' or deal == 'daily':
        request_json.update({'offer_price.price_day':json})
    return request_json

async def select_ground(kind:str,type:int,request_json:dict):
    if kind != 'house' and kind != 'ground':
        return request_json
    if type:
        request_json.update({'offer_object.ground_type':type})
    return request_json

async def select_city(city:str,request_json:dict):
    if city:
        request_json.update({'offer_object.city':city})
    return request_json

async def select_commercy(typeCommercy:str,request_json:dict):
    if not typeCommercy:
        return request_json
    request_json.update({'offer_object.office_type':typeCommercy})
    return request_json

async def select_size(kind:str,sizeFrom:int,sizeTo:int,request_json:dict):
    if sizeTo == 0 and sizeFrom == 0:
        return request_json
    if kind == 'apartment' or kind == 'commercy':
        request_json.update({'offer_object.area':{'$gte':sizeFrom, '$lte':sizeTo}})
    if kind == 'room':
        request_json.update({'offer_object.area_room': {'$gte': sizeFrom, '$lte': sizeTo}})
    if kind == 'ground' or kind == 'house':
        request_json.update({'offer_object.area_land': {'$gte': sizeFrom, '$lte': sizeTo}})
    if kind == 'building':
        request_json.update({'offer_object.area_building': {'$gte': sizeFrom, '$lte': sizeTo}})
    return request_json

async def get_offer(offer):
    offer['date'] = datetime.datetime.fromtimestamp(int(offer['date'])).strftime("%d.%m.%Y %H:%M")
    agent = False
    if offer['offer_price'].get('deposit') or offer['offer_price'].get('percentageTransaction'):
        agent = True
    price = offer['offer_price'].get('price')

    if offer['offer_price'].get('deal') == 'rent_long':
        price = offer['offer_price'].get('price_mounth')

    if offer['offer_price'].get('deal') == 'rent_day':
        price = offer['offer_price'].get('price_day')

    price_m2 = 0
    if offer['offer_object'].get('object') == 'apartment' or \
            offer['offer_object'].get('object') == 'office':
        price_m2 = float(price/offer['offer_object'].get('area'))

    if offer['offer_object'].get('object') == 'room':
        price_m2 = float(price/offer['offer_object'].get('area_room'))

    if offer['offer_object'].get('object') == 'house' or \
            offer['offer_object'].get('object') == 'ground':
        price_m2 = float(price/offer['offer_object'].get('area_land'))

    if offer['offer_object'].get('object') == 'building':
        price_m2 = float(price/offer['offer_object'].get('area_building'))
    list_images = []
    if len(offer['offerPhothos']) <4:
        return
    for i in range(4):
        list_images.append({'imgName':"https://mirllex.site/img/" + offer['offerPhothos'][i].get('imgName')})
    if len(offer['offerDescription']) > 300:
        offer['offerDescription'] = offer['offerDescription'][:300] + "..."
    if offer['user_avatar'] != "":
       offer['user_avatar'] = "https://mirllex.site/avatar/" + offer['user_avatar']
    return {"id":offer['_id'],
          'map_marker':offer['map_marker'],
          "userInfo":offer['userInfo'],
          "tel":offer['tel'],
          "title":offer['title'],
          "address":offer['map_address'],
          "price":price,
          "price_m2":round(price_m2,2),
          "description":offer['offerDescription'],
          "images":list_images,
          "is_agent":agent,
          'view':offer['view'],
          "date":offer['date'],
          "user_avatar":offer['user_avatar']}

async def select_pages(table,request_json:dict):
    pages = await table.count_documents(request_json)
    if pages % 20 == 0:
        pages = pages // 20
    else:
        pages = pages // 20 + 1
    return pages

async def select_offers(kind:str,type:str,object:str,repair:str,pagina:int,table):
    list_offers = []
    if kind == "commercy":
        async for post in table.find({"offer_object.office_type":object}).sort('date',-1):
            post['date'] = datetime.datetime.fromtimestamp(post['date']).strftime("%d.%m.%Y %H:%M")
            list_offers.append(post)
        return list_offers
    request_json = await select_kind(kind,type,repair)
    request_json = await select_count_rooms(request_json, object)
    response = {}
    list_offers = []
    async for post in table.find(request_json).sort('date', -1).skip((pagina-1) * 20).limit(20):
        list_offers.append(await get_offer(post))
    pages = await select_pages(table,request_json) 
    response = {"list_offers":list_offers,"pages": pages}
    return response

async def select_filter_offers(filter_offers:Filter_offers,table,page:int):
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
    request_json = await select_city(filter_offers.cities.get('value'),request_json)
    request_json = await select_ground(filter_offers.objects.get('value'),
                                       filter_offers.typeGround.get('value'),
                                       request_json)
    request_json =await select_commercy(filter_offers.typeCommercy.get('value'),request_json)
    request_json.update({"activ":1})
    response = {}
    list_offers = []
    async for post in table.find(request_json).sort('date', -1).skip((page-1) * 20).limit(20):
        if post["activ"] == 1:
            list_offers.append(await get_offer(post))
    pages = await select_pages(table,request_json) 
    response = {"list_offers":list_offers,"pages": pages}
    return response
