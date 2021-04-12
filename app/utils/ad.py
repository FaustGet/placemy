from config.mongodb import db
from utils.object_commercy import *
from utils.object_living import *
from utils.price__type import *


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

async def get_offer_price(type,offerPrice):
    if type == "sell":
        return await get_offer_sell(offerPrice)
    if type == "rent_long":
        return await get_rent_long(offerPrice)
    if type == "rent_day":
        return await get_rent_day(offerPrice)
    return {}

async def push_offerdb(estate,offer):
    if estate == "living":
        if offer.get('offer_price').get('deal') == "sell":
            await db.sell_living.insert_one(offer)
            return
        if offer.get('offer_price').get('deal') == "rent_long":
            await db.rent_long_living.insert_one(offer)
            return
        if offer.get('offer_price').get('deal') == "rent_day":
            await db.rent_day_living.insert_one(offer)
            return
        return
    if estate == "commercy":
        if offer.get('offer_price').get('deal') == "sell":
            await db.sell_commercy.insert_one(offer)
            return
        if offer.get('offer_price').get('deal') == "rent_long":
            await db.rent_long_commercy.insert_one(offer)
            return
        if offer.get('offer_price').get('deal') == "rent_day":
            await db.rent_day_commercy.insert_one(offer)
            return
    return


async def get_offer(id: str):
    id_list = id.split("-")
    try:
        estate = id_list[0]
        deal = id_list[1]
        if estate == "living":
            if deal == "sell":
                return db.sell_living.find_one({"_id": id})
            if deal == "rent_long":
                return await db.rent_long_living.find_one({"_id": id})
            if deal == "rent_day":
                return await db.rent_day_living.find_one({"_id": id})

        if estate == "commercy":
            if deal == "sell":
                return await db.sell_commercy.find_one({"_id": id})
            if deal == "rent_long":
                return await db.rent_long_commercy.find_one({"_id": id})
            if deal == "rent_day":
                return await db.rent_day_commercy.find_one({"_id": id})
        return ""
    except:
        return ""
