from twilio.rest import Client
from dotenv import load_dotenv
import os

PHONE_NUMBER = "+18044947762"
APP_SID= "MG190f52ced38f400b2ee059f72dacdff6"

load_dotenv()
TOKEN = str(os.getenv('TOKEN'))
SID = str(os.getenv('SID'))

def sendMessage(body, number):
    client = Client(SID, TOKEN)
    client.messages.create(to=number, from_=PHONE_NUMBER, body=body, messaging_service_sid=APP_SID)


    