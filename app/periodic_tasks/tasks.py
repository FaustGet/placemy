import time
from timeloop import Timeloop
import datetime
from pymongo import MongoClient

import os
import logging
logging.basicConfig(filename="sample.log", level=logging.INFO)
client = MongoClient('mongo', 27017, username='root', password='example')
db = client.realty
list_db = [db.rent_day_commercy,
           db.rent_day_living,
           db.rent_long_commercy,
           db.rent_long_living,
           db.sell_commercy,
           db.sell_living]
tl = Timeloop()


@tl.job(interval=datetime.timedelta(seconds=1800))
def check_images():
    date = datetime.datetime.now()
    print("kek")
    for post in db.temp_img.find():
        if post['date'] < int(date.timestamp()):
            db.temp_img.delete_one({"name":post['name']})
            try:
                with open('/app/images/' + post['name'], "wb") as buffer:
                   os.remove(buffer.name)
                with open('/app/images_services/' + post['name'], "wb") as buffer:
                   os.remove(buffer.name)
                      
            finally:
                logging.info(post['name'])

#@tl.job(interval=datetime.timedelta(hours=24))
#def check_offer():
#    date = datetime.datetime.now()
#    print("Delete offer")

#    for table in list_db:
#        for post in table.find():
#            if  int(date.timestamp() - post['date'] > ):

#                db.temp_img.delete_one({"name":post['name']})
#                try:
#                with open('/app/images/' + post['name'], "wb") as buffer:
#                   os.remove(buffer.name)
#            finally:
#                logging.info(post['name'])

tl.start(block=True)
