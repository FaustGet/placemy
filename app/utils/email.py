import smtplib
import ssl
import random
from email.mime.text import MIMEText
from email.header import Header
from config import email
from fastapi import  HTTPException
from config.sms_service import Sms_service
from hashlib import sha256
import requests

async def send_mes(phone_number: str, code:str):
    try:
        phone_number = phone_number.replace("(","").replace(")","").replace("+","").replace("-","").replace(" ","")
        txn_id = str(random.randint(100000, 999999))
        hash = f'{txn_id};{Sms_service.LOGIN};{Sms_service.FROM};{phone_number};{Sms_service.pass_salt_hash}'
        sha_str = sha256(hash.encode('utf-8')).hexdigest()
        message = f'Maidon.tj: {code} - ваш код для подтверждения телефона'
        response = requests.get(f'https://api.osonsms.com/sendsms_v1.php?login={Sms_service.LOGIN}&from={Sms_service.FROM}'
                                f'&phone_number={phone_number}&msg={message}&txn_id={txn_id}&str_hash={sha_str}')
        return True
    except:
        raise HTTPException(status_code=503)

