import motor.motor_asyncio
url = "mongodb://root:example@mirllex.site:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false"
client = motor.motor_asyncio.AsyncIOMotorClient(url)
db = client.realty
list_db = [db.rent_day_commercy,
           db.rent_day_living,
           db.rent_long_commercy,
           db.rent_long_living,
           db.sell_commercy,
           db.sell_living]

list_db_user = [db.rent_day_living,
               db.rent_long_living,
               db.sell_living]

list_db_user_commercy = [db.rent_day_commercy,
               db.rent_long_commercy,
               db.sell_commercy]
