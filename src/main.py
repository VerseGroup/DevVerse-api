# python imports
import os
from urllib import request
import uuid
from src.requests import *

# external imports 
from fastapi import FastAPI


#postgres server
from src.postgres.crud import Backend_Interface


# startup
app = FastAPI()

####### ROUTES [GENERAL] #######

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 

@app.get("/home", status_code=200)
async def home():
    return "home"



# post github data
@app.post("/data", status_code=200)
async def scrape_(request: OauthPostRequest):
    return request