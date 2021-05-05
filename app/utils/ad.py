from utils.object_commercy import *
from utils.object_living import *
from utils.price__type import *
from static.Dictionary import *
from utils.filter import select_table
from fastapi import HTTPException
import uuid
import datetime


async def get_offer_object(object_living, object_commercy, offerObject):
    if object_commercy == "office":
        return await get_office(offerObject)
    if object_commercy == "building":
        return await get_building(offerObject)
    if object_living == "apartment":
        return await get_apartment(offerObject)
    if object_living == "room":
        return await get_room(offerObject)
    if object_living == "house":
        return await get_house(offerObject)
    if object_living == "ground":
        return await get_ground(offerObject)
    return {}

 
async def get_offer_price(type, offerPrice):
    if type == "sell":
        return await get_offer_sell(offerPrice)
    if type == "rent_long":
        return await get_rent_long(offerPrice)
    if type == "rent_day":
        return await get_rent_day(offerPrice)
    return {}


async def push_offerdb(estate, offer):
    id = str(uuid.uuid4())
    offer.update({"_id": estate + "-" + offer.get('offer_price').get('deal') + "-" + id})
    table = await select_table(offer.get('offer_price').get('deal'), estate)
    await table.insert_one(offer)
    return


async def get_title(offer):
    title = ""
    if offer.get('object') == 'apartment':
        title = f"{offer.get('count_rooms')}-комн. кв., {offer.get('area')}м², {offer.get('floor')}/{offer.get('floorsHouse')} этаж."
    if offer.get('object') == 'room':
        title = f"{offer.get('count_rooms_rent')}-комн., {offer.get('area_room')}м², {offer.get('floor')}/{offer.get('floorsHouse')} этаж."
    if offer.get('object') == 'house':
        title = f"{offer.get('count_rooms')}-км. дом., {offer.get('area_land')}м², {offer.get('floorsHouse')} этаж."
    if offer.get('object') == 'ground':
        title = f"{ground_type.value.get(offer.get('ground_type'))}, {offer.get('area_land')}м²"
    if offer.get('object') == 'office':
        title = f"{office_type.value.get(offer.get('office_type'))}, {offer.get('area')}м²"
    if offer.get('object') == 'building':
        title = f"{offer.get('area_building')}м², {offer.get('floors_building')} э."
    return title


async def get_price(offer):
    price = offer['offer_price'].get('price')
    if offer['offer_price'].get('deal') == 'rent_long':
        price = offer['offer_price'].get('price_mounth')
    if offer['offer_price'].get('deal') == 'rent_day':
        price = offer['offer_price'].get('price_day')
    return price


async def get_price_m2(price, offer, deal):
    price_m2 = 0
    if offer['offer_object'].get('object') == 'apartment' or \
            offer['offer_object'].get('object') == 'office':
        price_m2 = float(price / offer['offer_object'].get('area'))

    if offer['offer_object'].get('object') == 'room':
        price_m2 = float(price / offer['offer_object'].get('area_room'))

    if offer['offer_object'].get('object') == 'house' or \
            offer['offer_object'].get('object') == 'ground':
        price_m2 = float(price / offer['offer_object'].get('area_land'))

    if offer['offer_object'].get('object') == 'building':
        price_m2 = float(price / offer['offer_object'].get('area_building'))

    return price_m2


async def get_offer_on_id(id: str):
    try:
        id_list = id.split("-")
        estate = id_list[0]
        deal = id_list[1]
        table = await select_table(deal, estate)
        offer = await table.find_one({"_id": id})
     
        if offer:
            if offer['activ'] == 0:
                return ""
            if offer['offer_object']['object'] == 'apartment' or offer['offer_object']['object'] == 'room':
                offer['offer_object']['building_type'] = building_type.value.get(offer['offer_object']['building_type'])
                offer['offer_object']['building_renovation'] = building_renovation.value.get(
                    offer['offer_object']['building_renovation'])

            if offer['offer_object']['object'] == 'house':
                offer['offer_object']['ground_type'] = ground_type.value.get(offer['offer_object']['ground_type'])
                offer['offer_object']['building_renovation'] = building_renovation.value.get(
                    offer['offer_object']['building_renovation'])

            if offer['offer_object']['object'] == 'ground':
                offer['offer_object']['ground_type'] = ground_type.value.get(offer['offer_object']['ground_type'])

            if offer['offer_object']['object'] == 'office':
                offer['offer_object']['office_type'] = office_type.value.get(offer['offer_object']['office_type'])

            price = await get_price(offer)
            price_m2 = await get_price_m2(price, offer, deal)
            offer['price_m2'] = round(price_m2, 2)

            agent = False

            if offer['offer_price'].get('deposit') or offer['offer_price'].get('percentageTransaction'):
                agent = True
            offer['is_agent'] = agent
            offer['offer_object']['object'] = type_objects.value.get(offer['offer_object']['object'])
            offer['date'] = datetime.datetime.fromtimestamp(offer['date']).strftime("%d.%m.%Y %H:%M")
            offer['offer_object']['city'] = city_type.value.get(offer['offer_object']['city'])
            if deal == "sell":
                offer['offer_price']['type_sell'] = type_sell_data.value.get(offer['offer_price']['type_sell'])
            if deal == "rent_long":
                offer['offer_price']['for_who'] = for_who_data.value.get(offer['offer_price']['for_who'])
                offer['offer_price']['prepayment'] = prepayment_data.value.get(offer['offer_price']['prepayment'])
            if deal == 'rent_day':
                offer['offer_price']['for_who'] = for_who_data.value.get(offer['offer_price']['for_who'])

            list_images = []
            for post in offer['offerPhothos']:
                list_images.append({'imgName': "https://mirllex.site/img/" + post.get('imgName')})
            offer['offerPhothos'] = list_images
            if offer['user_avatar'] != "":
                offer['user_avatar'] = "https://mirllex.site/avatar/" + offer['user_avatar']
            offer['view'] = offer['view'] + 1  
            await table.update_one({"_id":offer['_id']},{"$set":{"view":offer['view']}})
            return offer
        else:
            raise HTTPException(status_code=404)
             
    except:
        raise HTTPException(status_code=404)


async def Get_info(obj:str,value):

    if obj == "object":
         value = type_objects.value.get(value)

    if obj == 'ground_type':
         value = ground_type.value.get(value)

    if obj == 'office_type':
         value = office_type.value.get(value)

    if obj == "building_type":
         value = building_type.value.get(value)

    if obj == "building_renovation":
         value = building_renovation.value.get(value)

    if obj == "city":
         value = city_type.value.get(value)
    return str(value)

async def Get_info_price(obj:str,value):


    if obj == "deal":
         value = deal_type.value.get(value)
    if obj == "type_sell":
         value = type_sell_data.value.get(value)
    if obj == "prepayment":
         value = prepayment_data.value.get(value)
    if obj == "for_who":
         value = for_who_data.value.get(value)

    return str(value)

