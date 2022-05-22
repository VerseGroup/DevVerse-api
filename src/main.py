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
from src.parse_webhook import parse_check_run, parse_push

#postgres server
from src.postgres.models import User, Task, TodoList
from src.postgres.crud import Backend_Interface

# startup
app = FastAPI()
interface = Backend_Interface()

do_all_texts = False

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
    
    if 'check_run' in body_data:
        body = parse_check_run(body_data)
    if 'push' in body_data:
        body = parse_push(body_data)
    else:
        body = None

    if body is not None:        
        for number in NUMBERS:
            sendMessage(body, number)
    else:
        if do_all_texts:
            for number in NUMBERS:
                keys = []
                for key in body_data:
                    keys.append(key)
                sendMessage(f"not a relevant update to {repo}: {keys}", number)
            
# create sign up 
@app.post("/addUser", status_code=200)
async def addUser(request: AddUserRequest):
    # add user to database

    # if oauth exists return user coresponding to oauth.
    headers = {
        "Authorization": f"token {request.oauth_token}",
    }

    r = requests.get("https://api.github.com/user", headers=headers)

    data_dict = r.json()


    username = data_dict['login']
    email = data_dict['email']
    display_name = data_dict['name']
    

    user = User(username, email, request.phone_number, display_name, request.oauth_token)
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

@app.get("/changetextsettings", status_code=200)
async def changeTextSettings():
    global do_all_texts
    do_all_texts = not do_all_texts
    return {"message": f"text settings changed to {do_all_texts}"}
