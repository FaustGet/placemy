
async def get_office(offerObject):
    return {
        "object": "office",
        "area": int(offerObject.get("inputs").get("area").get("value")),
        "office_type": offerObject.get("selects").get("office_type").get("value"),
    }

async def get_building(offerObject):
    return {
        "object":"building",
        "area_building": int(offerObject.get("inputs").get("area_building").get("value")),
        "floors_building": offerObject.get("inputs").get("floors_building").get("value"),
    }