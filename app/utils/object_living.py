async def get_apartment(offerObject):
    return {
        "object": "apartment",
        "area": offerObject.get("inputs").get("area").get("value"),
        "count_rooms": offerObject.get("inputs").get("count_rooms").get("value"),
        "floor": offerObject.get("inputs").get("floor").get("value"),
        "floorsHouse": offerObject.get("inputs").get("floorsHouse").get("value"),
        "building_type": offerObject.get("selects").get("building_type").get("value"),
        "building_renovation": offerObject.get("selects").get("building_renovation").get("value"),
    }

async def get_room(offerObject):
    return {
        "object": "room",
        "area": offerObject.get("inputs").get("area").get("value"),
        "area_room": offerObject.get("inputs").get("area_room").get("value"),
        "count_rooms": offerObject.get("inputs").get("count_rooms").get("value"),
        "count_rooms_rent": offerObject.get("inputs").get("count_rooms_rent").get("value"),
        "floor": offerObject.get("inputs").get("floor").get("value"),
        "floorsHouse": offerObject.get("inputs").get("floorsHouse").get("value"),
        "building_type": offerObject.get("selects").get("building_type").get("value"),
        "building_renovation": offerObject.get("selects").get("building_renovation").get("value"),
    }

async def get_house(offerObject):
    return {
        "object": "house",
        "area_land": offerObject.get("inputs").get("area_land").get("value"),
        "area_house": offerObject.get("inputs").get("area_house").get("value"),
        "count_rooms": offerObject.get("inputs").get("count_rooms").get("value"),
        "floorsHouse": offerObject.get("inputs").get("floorsHouse").get("value"),
        "ground_type": offerObject.get("selects").get("ground_type").get("value"),
        "building_renovation": offerObject.get("selects").get("building_renovation").get("value"),
    }

async def get_ground(offerObject):
    return {
        "object": "ground",
        "area_land": offerObject.get("inputs").get("area_land").get("value"),
        "ground_type": offerObject.get("selects").get("ground_type").get("value"),
    }