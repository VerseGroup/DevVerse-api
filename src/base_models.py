from pydantic import BaseModel

class OauthPostRequest(BaseModel):
    client_id: str
    client_secret: str
    code: str
    redirect_uri: str

class RelayRequest(BaseModel):
    endpoint: str
    data: str
    method: str

class AddUserRequest(BaseModel):
    username: str
    password: str
    email: str
    phone: str
    display_name: str
    github_oauth_token:str