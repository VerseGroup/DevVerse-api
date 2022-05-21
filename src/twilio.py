import os
from twilio.rest import Client
from datetime import datetime
from dotenv import load_dotenv

PHONE_NUMBER = "+18044947762"

load_dotenv()
TOKEN = str(os.getenv('TOKEN'))
SID = str(os.getenv('SID'))

def sendMessages(body, number):

    client = Client(SID, TOKEN)

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    client.messages.create(to=number, from_=PHONE_NUMBER, body=body)
    client.messages.create(to=number, from_=PHONE_NUMBER, body=body) 