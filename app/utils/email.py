import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header
from config import email
from fastapi import  HTTPException


async def send_mes(user_email: str, code:str):
    try:
        server = smtplib.SMTP('mirllex.site',25)
        server.login(email.Config.LOGIN_EMAIL, email.Config.PASSWORD_EMAIL)
        from utils.authentication import create_access_token
        access_token = await create_access_token(data={"email": user_email,"code":code}, expires_delta=60)
        msg = MIMEText(email.Config.EMAIL_TEXT + " https://mirllex.site/account/activate?access=" + str(access_token), 'plain', 'utf-8')
        msg['Subject'] = Header(email.Config.EMAIL_TEXT, 'utf-8')
        msg['From'] = email.Config.LOGIN_EMAIL
        msg['To'] = user_email
        server.sendmail(email.Config.LOGIN_EMAIL, user_email, msg.as_string())
        server.quit()
        return True
    except:
        raise HTTPException(status_code=503)

async def send_mes_reset_pass(user_email: str, code:str):
    try:
        server = smtplib.SMTP('mirllex.site',25)
        server.login(email.Config.LOGIN_EMAIL, email.Config.PASSWORD_EMAIL)
        from utils.authentication import create_access_token
        access_token = await create_access_token(data={"email": user_email,"code":code}, expires_delta=60)
        msg = MIMEText(email.Config.EMAIL_TEXT_PWD + " https://mirllex.site/account/restorepassword?pwd=" + str(access_token), 'plain', 'utf-8')
        msg['Subject'] = Header(email.Config.EMAIL_TEXT_PWD, 'utf-8')
        msg['From'] = email.Config.LOGIN_EMAIL
        msg['To'] = user_email
        server.sendmail(email.Config.LOGIN_EMAIL, user_email, msg.as_string())
        server.quit()
        return True
    except:
        raise HTTPException(status_code=503)
