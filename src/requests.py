from pydantic import BaseModel

class OauthPostRequest(BaseModel):
    client_id: str
    client_secret: str
    code: str
    redirect_uri: str

class Scrape(BaseModel):
    endpoint: str
    data: str
    method: str