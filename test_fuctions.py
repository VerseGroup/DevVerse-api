import requests
import os
from dotenv import load_dotenv
load_dotenv()

Oauth = os.getenv('OAUTH_TOKEN')
phone_number = "+19143348636"



def test_sign_in():
    json = {
        "oauth_token" : Oauth
    }

    r = requests.post("https://devverse-server.herokuapp.com/signIn", json=json)

    print(r.content.decode("utf-8"))

def test_add_user():
    json = {
        "oauth_token" : Oauth,
        "phone_number" : phone_number
    }

    r = requests.post("https://devverse-server.herokuapp.com/addUser", json=json)

    print(r.content.decode("utf-8"))

test_add_user()