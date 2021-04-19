import time
from timeloop import Timeloop
import datetime
from pymongo import MongoClient
import os
import logging
logging.basicConfig(filename="sample.log", level=logging.INFO)
client = MongoClient('mongo', 27017, username='root', password='example')
db = client.realty

tl = Timeloop()


@tl.job(interval=datetime.timedelta(seconds=1800))
def check_images():
    date = datetime.datetime.now()
    for post in db.temp_img.find():
        if post['date'] < int(date.timestamp()):
            db.temp_img.delete_one({"name":post['name']})
            try:
                with open('/app/images/' + post['name'], "wb") as buffer:
                   os.remove(buffer.name)
            finally:
                logging.info(post['name'])

tl.start(block=True)
