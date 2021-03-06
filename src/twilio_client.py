from twilio.rest import Client
from dotenv import load_dotenv
import os
import sys

# add local path to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from phone_numbers import NUMBERS
except:
    NUMBERS = []

PHONE_NUMBER = "+18044947762"
APP_SID= "MG190f52ced38f400b2ee059f72dacdff6"

try:
    load_dotenv()
except:
    pass

TOKEN = str(os.environ['TOKEN'])
SID = str(os.environ['SID'])

def sendMessage(body, number):
    client = Client(SID, TOKEN)
    client.messages.create(to=number, from_=PHONE_NUMBER, body=body, messaging_service_sid=APP_SID)

if __name__ == "__main__":
    for number in NUMBERS:
        sendMessage("KANYE WEST SAYS HELLO", number)

    