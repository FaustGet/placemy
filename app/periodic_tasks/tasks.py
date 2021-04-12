import time
from timeloop import Timeloop
import datetime
from pymongo import MongoClient
import os
client = MongoClient('mongo', 27017, username='root', password='example')
db = client.realty

tl = Timeloop()


@tl.job(interval=datetime.timedelta(seconds=5))
def scheck_images():
    date = datetime.datetime.now()
    # for post in db.temp_img.find():
    #     if post['date'] < int(date.timestamp()):
    #         db.temp_img.remove({"name":post['name']})
    #         try:
    #             with open('/app/images/' + post['name'], "wb") as buffer:
    #                 os.remove(buffer.name)
    #         finally:
    #             print("delete - ",post['name'])
    print("kek")

tl.start(block=True)
