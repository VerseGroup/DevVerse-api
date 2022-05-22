from pydantic import BaseModel

class OauthPostRequest(BaseModel):
    client_id: str
    client_secret: str
    code: str
    redirect_uri: str

class RelayRequest(BaseModel):
    endpoint: str
    method: str
    oauth_token: str

class AddUserRequest(BaseModel):
    oauth_token: str
    phone_number: str

class LoginRequest(BaseModel):
    oauth_token: str

class AddTaskRequest(BaseModel):
    task_name: str
    task_description: str
    oauth_token: str
    
class AddWebhookRequest(BaseModel):
    oauth_token: str
    repo: str

class GetTasksRequest(BaseModel):
    todo_list_id: int

class GetTodoListsRequest(BaseModel):
    oauth_token: str

class AddTodoListRequest(BaseModel):
    todo_list_name: str
    todo_list_description: str
    oauth_token: str

class AddIdeaRequest(BaseModel):
    idea_name: str
    idea_description: str
    oauth_token: str

class ViewIdeasRequest(BaseModel):
    oauth_token: str

class EditIdeaRequest(BaseModel):
    idea_id: int
    idea_name: str
    idea_description: str
    idea_completed: bool
    user_id: int
