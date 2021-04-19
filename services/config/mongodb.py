import motor.motor_asyncio
url = "mongodb://root:example@mirllex.site:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false"
client = motor.motor_asyncio.AsyncIOMotorClient(url)
db = client.realty