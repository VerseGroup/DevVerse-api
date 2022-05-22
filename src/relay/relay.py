# utils
from src.relay.utils import get_url
import requests

def relay(endpoint, method, oauth_token):
    url = get_url(endpoint)

    header = {
        "Authorization": f"token {oauth_token}",
    }

    if method == "GET":
        r = requests.get(url, headers=header)
    elif method == "POST":
        r = requests.post(url, headers=header)

    return r
   


