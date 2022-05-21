# python imports
import os
import uuid

# external imports 
from fastapi import FastAPI


#postgres server
from postgres.crud import Backend_Interface


# startup
app = FastAPI()

####### ROUTES [GENERAL] #######

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 

@app.get("/home", status_code=200)
async def ping():
    return {"message": "home"}