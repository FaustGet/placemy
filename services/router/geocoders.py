from fastapi import APIRouter

from config import server
from models.geocoder import Geocoder_reverse, Geocoder_point
from geopy.geocoders import Nominatim

router = APIRouter(prefix=server.Server_config.prefix,
                   responses = server.Server_config.responses,
                   tags=['geocoder'])
 
class Geocod(object):
    address = "Таджикистан"

@router.post("/offer_geocoder_reverse")
async def geocoder_reverse(point:Geocoder_reverse):
    try:
        geolocator = Nominatim(user_agent="mirllex")
        location = geolocator.reverse(f"{str(point.x)}, {str(point.y)}")
        return {"map_address":str(location.address)}
    except:
        return {"map_address":""}

@router.post("/offer_geocoder_geocode")
async def geocoder_geocode(point:Geocoder_point):
    try:
        
        point.map_address = point.map_address +" " +  Geocod.address
        print(point)
        geolocator = Nominatim(user_agent="mirllex")
        location = geolocator.geocode(point.map_address)
        print(location.address)
        return [{'value':location.address,"coords":[location.latitude,location.longitude]}]
        
        #print(location.latitude, location.longitude)
        #return {location.latitude,location.longitude}
    except:
        return [{'value':""}]
