# python imports
import os
from urllib import request
import uuid
from src.requests import *

# external imports 
from fastapi import FastAPI

# internal imports
from src.relay.relay import relay

#postgres server
from src.postgres.crud import Backend_Interface

# startup
app = FastAPI()

####### ROUTES [GENERAL] #######

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 

####### ROUTES [MAIN] #######

@app.post("/relay", status_code=200)
async def _relay(request: RelayRequest):
    try:
        relay(request)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@app.post("/adduser", status_code=200)
async def adduser(request: AddUserRequest):
    # add user to database
    return {"message": "user added"}
 
# post github data
@app.post("/data", status_code=200)
async def scrape_(request: OauthPostRequest):
    return request


    