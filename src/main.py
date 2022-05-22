# python imports
from fastapi import FastAPI, Request
from urllib import request
from src.base_models import *
import requests
import uuid
import json
import os

# internal imports
from src.relay.relay import relay
from src.phone_numbers import NUMBERS
from src.twilio_client import sendMessage
from src.parse_webhook import parse_check_run

#postgres server
from src.postgres.models import User, Task, TodoList
from src.postgres.crud import Backend_Interface

# startup
app = FastAPI()
interface = Backend_Interface()


####### ROUTES [Basic] #######


@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 


####### ROUTES [MAIN] #######


@app.post("/relay", status_code=200)
async def _relay(request: RelayRequest):
    try:
        response = relay(request)
        return {"message": "success", "response": response}
    except Exception as e:
        return {"message": "error", "exception" : str(e)}

@app.post("/adduser", status_code=200)
async def adduser(request: AddUserRequest):
    # add user to database
    return {"message": "user added"}
 
# post github data (testing)
@app.post("/data", status_code=200)
async def scrape_(request: OauthPostRequest):
    return request

# recieve data from github
@app.post("/webhook", status_code=200)
async def webhook(request: Request):
    
    body_data = await request.json()

    # univeral data
    repo = body_data['repository']['name']
    
    if 'check_suite' in body_data:
        body = parse_check_run(body_data)
    else:
        body = None

    if body is not None:        
        for number in NUMBERS:
            sendMessage(body, number)

# create sign up 
@app.post("/addUser", status_code=200)
async def addUser(Oauth_Token: str, phone_number: str):
    # add user to database

    # if oauth exists return user coresponding to oauth.
    headers = {
        "Authorization": f"token {Oauth_Token}",
    }

    r = requests.get("https://api.github.com/user", headers=headers)

    data_dict = r.content.decode("utf-8")


    username = data_dict['login']
    email = data_dict['email']
    display_name = data_dict['name']
    github_oauth_token = data_dict['id']

    user = User(username, email, phone_number, display_name, github_oauth_token)
    interface.create_user(user)
    return user.serialize()


# sign in 
@app.post("/signIn", status_code=200)
async def signIn(Oauth_Token: str):
    # if oauth exists return user coresponding to oauth.

    user = interface.fetch_user_by_oauth(Oauth_Token)
    if user is None:
        return {"message": "user does not exist"}
    else:
        return User(*user).serialize()
