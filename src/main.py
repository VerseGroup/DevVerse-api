# python imports
import os
from urllib import request
import uuid
from src.requests import *
import json

# external imports 
from fastapi import FastAPI, Request

# internal imports
from src.relay.relay import relay

#postgres server
from src.postgres.models import User, Task, TodoList
from src.postgres.crud import Backend_Interface



# startup
app = FastAPI()
interface = Backend_Interface()

####### ROUTES [GENERAL] #######

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
 
# post github data
@app.post("/data", status_code=200)
async def scrape_(request: OauthPostRequest):
    return request

# recieve data from github
@app.post("/webhook", status_code=200)
async def webhook(request: Request):
    json = request.json
    
@app.post("/addUser", status_code=200)
async def addUser(request: AddUserRequest):
    # add user to database
    user = User(request.username, request.email, request.password, request.phone, request.display_name, request.github_oauth_token)
    interface.create_user(user)
    return {"message": "user added"}

