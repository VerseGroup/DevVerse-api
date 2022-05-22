# python imports
from fastapi import FastAPI, Request
from urllib import request
from src.base_models import *
import requests
import uuid
import json
import os

# internal imports
from src.relay.relay import relay_
from src.phone_numbers import NUMBERS
from src.twilio_client import sendMessage
from src.parse_webhook import *

#postgres server
from src.postgres.models import User, Task, TodoList, Idea
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
        response = relay_(request.endpoint, request.method, request.oauth_token)
        return {"message": "success", "response": response.content}
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
    sender = body_data['sender']['login']

    try:
        phone = interface.get_user(sender)[3]
    except:
        phone = None
    
    if 'check_run' in body_data:
        body = parse_check_run(body_data)
    if 'head_commit' in body_data:
        body = parse_push(body_data)
    if 'issue' in body_data:
        body = parse_issue(body_data)

    else:
        body = None

    if body is not None:        
        
        if phone is None:
            
            for number in NUMBERS:
                sendMessage(body, number)
        
        else:
            sendMessage(body, phone)
            sendMessage("sent", NUMBERS[0])
    
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
    name = data_dict['name']
    
    user = User(username, email, request.phone_number, name, request.oauth_token)

    try:
        id = interface.create_user(user)
        return {"id": id, "username": username, "email": email, "phone": request.phone_number, "name": name, "github_oauth_token": request.oauth_token}
    except Exception as e:
        return {"message": "error", "exception" : str(e)}


# sign in 
@app.post("/signIn", status_code=200)
async def signIn(request: LoginRequest):
    # if oauth exists return user coresponding to oauth.

    user = interface.fetch_user_by_oauth(request.oauth_token)
    if user is None:
        return {"message": "user does not exist"}
    else:
        
        id = user[0]
        username = user[1]
        email = user[2]
        phone = user[3]
        name = user[4]
        github_oauth_token = user[5]

        return {"id": id, "username": username, "email": email, "phone": phone, "name": name, "github_oauth_token": github_oauth_token}

#twilio config
@app.get("/changetextsettings", status_code=200)
async def changeTextSettings():
    global do_all_texts
    do_all_texts = not do_all_texts
    return {"message": f"text settings changed to {do_all_texts}"}


@app.post("/addTask", status_code=200)
async def addTask(request: AddTaskRequest):
    try:
        user_id = interface.fetch_user_id_by_oauth(request.oauth_token)
        if type(user_id) is not int:
            raise Exception("USER_ID WRONG TPYE YOU BUM in addTask")

        task = Task(request.task_name, False, request.task_description, user_id)
        interface.create_task(task)
        return {"message": "success"}
    except Exception as e:
        return {"message": "error", "exception" : str(e)}

@app.post("/getTasks", status_code=200)
async def getTasks(request: GetTasksRequest):
    try:
        #oauth_token   
        tasks = interface.fetch_task_by_todo_list_id(request.todo_list_id)
        return {"tasks": tasks}
    except Exception as e:
        return {"message": "error", "exception" : str(e)}

@app.post("/addWebhook", status_code=200)
async def addWebhook(request: AddWebhookRequest):
    repo = request.repo
    user = interface.fetch_user_by_oauth(request.oauth_token)
    
    if user is None:
        return {"message": "user does not exist"}

    username = user[1]

    URL = f"https://api.github.com/repos/{username}/{repo}/hooks"

    headers = {
        "accept": "application/vnd.github.v3+json",
        "Authorization": f"token {request.oauth_token}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = "{\"name\":\"web\",\"active\":true,\"events\":[\"push\",\"pull_request\",\"check_run\",\"issues\"],\"config\":{\"url\":\"https://devverse-server.herokuapp.com/webhook\",\"content_type\":\"json\",\"insecure_ssl\":\"0\"}}"

    response = requests.post(URL, data=data, headers=headers)

    return {"message": "success", "response": response.json()}
    

# idea models


@app.post("/addIdea", status_code=200)
async def addIdea(request: AddIdeaRequest):
    try:
        user_id = interface.fetch_user_id_by_oauth(request.oauth_token)
        if type(user_id) is not int:
            raise Exception("USER_ID WRONG TPYE YOU BUM in addIdea")
        idea = Idea(request.idea_name, request.idea_description, user_id)
        interface.create_idea(idea)
        return {"message": "success"}
    except Exception as e:
        return {"message": "error", "exception" : str(e)}

@app.post("/viewIdeas", status_code=200)
async def viewIdeas(request: ViewIdeasRequest):
    try:
        #user id from oauth
        user_id = interface.fetch_user_id_by_oauth(request.oauth_token)
        ideas = interface.fetch_ideas_by_user_id(user_id)
        return ideas
    except Exception as e:
        return {"message": "error", "exception" : str(e)}


@app.post("/editIdea", status_code=200)
async def editIdea(request: EditIdeaRequest):
    try:
        idea = Idea(request.idea_name, request.idea_description, request.user_id, request.idea_completed)
        interface.edit_idea(idea, request.idea_id)
    except Exception as e:
        return {"message": "error", "exception" : str(e)}