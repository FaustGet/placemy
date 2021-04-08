from time import sleep
from celery import Celery
from celery.utils.log import get_task_logger
import shutil
import asyncio
import os
import datetime
from pymongo import MongoClient
client = MongoClient('mongo', 27017, username='root', password='example')
db = client.realty



if not bool(os.getenv('DOCKER')):
    app = Celery('tasks', broker='pyamqp://user:user@127.0.0.1:5672//')
else:
    app = Celery('tasks', broker='pyamqp://user:user@rabbit:5672//')


celery_log = get_task_logger(__name__)



@app.task(name = "tasks.check_images")
def check_images():
    date = datetime.datetime.now()
    for post in db.temp_img.find():
        if post['date'] < int(date.timestamp()):
            db.temp_img.remove({"name":post['name']})
            try:
                with open('/app/images/' + post['name'], "wb") as buffer:
                    os.remove(buffer.name)
            finally:
                print("delete - ",post['name'])

app.conf.beat_schedule = {
    'test-task': {
        'task': 'tasks.check_images',  # instead 'show'
        'schedule': 7200.0
    },
}

app.conf.timezone = 'UTC'