from fastapi import APIRouter
from config import server
from config.mongodb import list_db,list_db_user
from models.Ad import *
from utils.ad import *
from utils.authentication import *
from static.Dictionary import info, price_info
from models.filters import *
from utils.filter import *
from utils.files import delete_files

router = APIRouter(prefix=server.Server_config.prefix,
                   responses=server.Server_config.responses,
                   tags=['ad'])


@router.post("/create_offer")
async def create_offer(new_ad: Place_an_ad, request: Request):
    user = await check_auth_user(request)
    try:
        advertisement = {"id_user": user['_id'],
                         "userInfo": f"{user['surname']}  {user['name']}",
                         "tel": user['tel'],
                         "map_address": new_ad.offerMap.get('map_address'),
                         "map_marker": new_ad.offerMap.get('map_marker')}

        offer_object = await get_offer_object(new_ad.offerType.get("object_living"),
                                              new_ad.offerType.get("object_commercy"),
                                              new_ad.offerObject)
        offer_price = await get_offer_price(new_ad.offerType.get('deal'), new_ad.offerPrice)
        offer_object.update({'city': new_ad.offerObject.get('selects').get('cities').get('value')})
        if new_ad.offerType.get('account') == 'agent':
            offer_price.update({"percentageTransaction":
                                    new_ad.offerPrice.get("inputs").get('percentageTransaction').get('value')})
        title = await get_title(offer_object)
        list_offerImages = []
        for post in new_ad.offerPhothos:
            image = await db.temp_img.find_one({"name": post.get('imgName')})
            if image:
                list_offerImages.append({"imgName": image['newName']})
                db.temp_img.delete_one({"name": post.get('imgName')})
        advertisement.update({'title': title,
                              "offer_object": offer_object,
                              "offer_price": offer_price,
                              "offerDescription": new_ad.offerDescription,
                              "date": int(datetime.datetime.now().timestamp()),
                              "offerPhothos": list_offerImages,
                              "user_avatar": user['avatar'],
                              "view":0,
                              "view_tel":0,
                              "activ": 0,
                              'note':""})
        await push_offerdb(new_ad.offerType.get("estate"), advertisement)
        return
    except:
        raise HTTPException(status_code=409)


@router.get("/get_offer/{id}")
async def get_offerID(id: str):
    try:
        offer = await get_offer_on_id(id)
        return offer
    except:
        raise HTTPException(status_code=404)


@router.post("/delete_offer")
async def delete_offer(del_offer: Delete_offer, request: Request):
    user = await check_auth_user(request) 
    try:
        user = await check_auth_user(request)
        if user == -1:
            return Response(status_code=401)
        id_list = del_offer.id.split("-")
        table = await select_table(id_list[1], id_list[0])
        offer = await table.find_one({"_id": del_offer.id})
        if offer == "":
            return Response(status_code=404)
        if offer['id_user'] == user['_id']:
            for image in offer['offerPhothos']:
                await delete_files(image.get('imgName'))
            if table != -1:
                await table.delete_one({"_id": del_offer.id})
        else:
            return Response(status_code=409)
    except:
        raise HTTPException(status_code=409)


@router.post("/get_filter_offers")
async def get_filter_offers(filter_offers: Filter_offers):
    try:
        table = await select_table(filter_offers.deals.get('value'), filter_offers.objects.get('value'))
        if table == -1:
            return []
        list_offer = await select_filter_offers(filter_offers, table, filter_offers.page)
        return list_offer
    except:
        return Response(status_code=409)


@router.get("/get_user_offers")
async def get_user_offers(request: Request):
    user = await check_auth_user(request)
    try:
        if user == -1:
            return []
        list_user_offer = []
        for table in list_db:
            async for offer in table.find({'id_user': user['_id']}):
                list_images = []
                for image in offer['offerPhothos']:
                    list_images.append({"imgSrc": "https://mirllex.site/img/" + image.get('imgName'),"imgName":image.get('imgName')})
                agent = False
                type_object = "living"
                if offer['offer_object'].get('object') == 'office' or offer['offer_object'].get('object') == 'build':
                    type_object = "commercy"
                if offer['offer_price'].get('deposit') or offer['offer_price'].get('percentageTransaction'):
                    agent = True
                object = offer['offer_object'].get('object')
                if offer['offer_object'].get('object') == 'office':
                    object = "commercy"
                deal = "buy"
                if offer['offer_price'].get('deal') == "rent_long":
                    deal = "rent"
                if offer['offer_price'].get('deal') == "rent_day":
                    deal = "daily"
                list_user_offer.append({"id": offer['_id'],
                                        "title": offer['title'],
                                        "object":object,
                                        "deal":deal,
                                        "description": offer['offerDescription'],
                                        'offerObject':offer['offer_object'],
                                        'offerPrice':offer['offer_price'],
                                        'photos': list_images,
                                        'view':offer['view'],
                                        'agent':agent,
                                        'state': offer['activ'],
                                        'type_object':type_object,
                                        'view_tel':offer['view_tel']})
        return list_user_offer
    except:
        return Response(status_code=409)


@router.post("/activ_offer")
async def aciv_offer(offer: activ_offer, request: Request):
    user = await check_auth_moderator(request)
    try:
        id_list = offer.id.split("-")
        table = await select_table(id_list[1], id_list[0])
        if table == -1:
            return
        offer_update = await table.find_one({"_id": offer.id})
        if offer_update:
            await table.update_one({"_id": offer.id}, {"$set": {"activ":offer.active}})
            if offer.note !="":
                chat = await db.chat.find_one({"user.id":'moderator',"title":offer_update['title']})
                print(chat)
                if chat:
                    await db.chat.update_one({"_id":chat['_id']},
                                              {"$push":{"message":{"user":'moderator',
                                                                   "text":offer.note,
                                                                   "check":False,
                                                                   "date":datetime.datetime.now().strftime('%H:%M - %m.%d.%Y')}}})
                else:
                   id_chat = str(uuid.uuid4())
                   await db.chat.insert_one({"_id":id_chat,
                                             "title":offer_update['title'],
                                             "image":offer_update['offerPhothos'][0].get("imgName"),
                                             "id_offer":offer_update['_id'],
                                             "unread": offer_update['id_user'],
                                             'user':[
                                                  {"id":"moderator","name":f"Moderator"},
                                                  {"id":offer_update['id_user'],"name":offer_update['userInfo']}],
                                             "message":[{"user":"moderator",
                                                         "text":offer.note,
                                                         "check":False,
                                                         "date":datetime.datetime.now().strftime('%H:%M - %m.%d.%Y')}]})


        return
    except:
        return Response(status_code=409)


@router.post("/change_offer")
async def offer_patch(offer: Offer_patch, request: Request):
    user = await check_auth_user(request)
    try:
        id_list = offer.id.split("-")
        estate = id_list[0]
        deal = id_list[1]
        table = await select_table(deal, estate)
        if table == -1:
            return
        if await table.find_one({"_id":offer.id}):
             list_images = []
             for img in offer.photos:
                 new_img = await db.temp_img.find_one({"name":img.get('imgName')})
                 if new_img:
                      list_images.append({"imgName":new_img['newName']})
                      await db.temp_img.delete_one({"name":img.get('imgName')})
                 else:
                      list_images.append({"imgName":img.get('imgName')})
             offer_object = await get_offer_object(offer.offerObject.get("object"),
                                             offer.offerObject.get("object"),
                                             offer.offerObject)
             
             offer_price = await get_offer_price(offer.offerPrice.get('deal'), offer.offerPrice)
             title = await get_title(offer_object)
             offer_object.update({'city': offer.offerObject.get('selects').get('cities').get('value')})
             
             request_json = {"offerDescription":offer.description,
                             "offerPhothos":list_images,"activ":False,
                             "offer_object":offer_object,
                             "offer_price":offer_price,
                             'title':title,
                             'activ':0}
             
                      
             await table.update_one({"_id":offer.id},{"$set":request_json})
             await db.chat.update_many({"id_offer":offer.id},
                                       {"$set":{"title":title,"image":list_images[0].get('imgName')}})
    except:
        return Response(status_code=409)

@router.get("/get_moder_offer")
async def get_moder_offer(request: Request):
    user = await check_auth_moderator(request)
    try:
       list_offer = []
       for table in list_db_user:
           async for offer  in table.find({'activ':0}):
               list_img = []
               for img in offer['offerPhothos']:
                   list_img.append({"imgName":"https://mirllex.site/img/" + img.get('imgName')})

               offer_object_text = ""
               for obj in offer['offer_object']:
                   offer_object_text += f"{info.value.get(obj)} - {await Get_info(obj,offer['offer_object'].get(obj))}\n\n"

               offer_price_text = ""
               for obj in offer['offer_price']:
                   offer_price_text += f"{price_info.value.get(obj)} - {await Get_info_price(obj,offer['offer_price'].get(obj))}\n\n"

               list_offer.append({"id":offer['_id'],
                              'title': offer['title'],
                              'map_address':offer['map_address'],
                              "offer_object": offer_object_text,
                              "offer_price": offer_price_text,
                              "offerDescription": offer['offerDescription'],
                              "offerPhothos": list_img})
       return list_offer
    except:
        return Response(status_code=409)

@router.get("/get_markers")
async def get_markers(request: Request):
    list_offer = []
    try:
        for table in list_db:
           async for offer  in table.find({'activ':1}):
               list_offer.append({"id":offer['_id'],
                                  "marker":offer['map_marker']})
        return list_offer
    except:
        return list_offer

@router.get("/get_map_offer/{id}")
async def get_map_offer(id:str):
    try:
        id_list = id.split("-")
        table = await select_table(id_list[1], id_list[0])
        offer = await table.find_one({"_id":id})

        if not offer:
            return Response(status_code=404)
        if offer['activ'] == 0:
            return Response(status_code=404)

        object = offer['offer_object'].get('object')
        if offer['offer_object'].get('object') == 'office':
             object = "commercy"
        deal = "buy"
        if offer['offer_price'].get('deal') == "rent_long":
             deal = "rent"
        if offer['offer_price'].get('deal') == "rent_day":
             deal = "daily"
        offer = await get_offer(offer)
        offer['object'] = object
        offer['deal'] = deal


        return offer
    except:
        return Response(status_code=409)



