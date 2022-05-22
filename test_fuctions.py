import requests
import os
from dotenv import load_dotenv
import psycopg2
load_dotenv()


Oauth = os.getenv('OAUTH_TOKEN')

phone_number = "+19143348636"

json = {
    "oauth_token" : Oauth
}


r = requests.post("https://devverse-server.herokuapp.com/signIn", json=json)

print(r.content.decode("utf-8"))
