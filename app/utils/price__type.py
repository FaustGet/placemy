async def get_offer_sell(offerPrice):
    return {
        "deal":"sell",
        "price": offerPrice.get("inputs").get("price").get("value"),
        "type_sell": offerPrice.get("selects").get("type_sell").get("value"),
    }

async def get_rent_long(offerPrice):
    return {
        "deal": "rent_long",
        "price_mounth": offerPrice.get("inputs").get("price_mounth").get("value"),
        "deposit": offerPrice.get("inputs").get("deposit").get("value"),
        "prepayment": offerPrice.get("selects").get("prepayment").get("value"),
        "for_who": offerPrice.get("selects").get("for_who").get("value"),
    }

async def get_rent_day(offerPrice):
    return {
        "deal": "rent_day",
        "price_day": offerPrice.get("inputs").get("price_day").get("value"),
        "for_who": offerPrice.get("selects").get("for_who").get("value"),
    }