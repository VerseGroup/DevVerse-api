# utils
from src.relay.utils import get_url
import requests

def relay(relay_request):
    url = get_url(relay_request.endpoint)
    data = relay_request.data
    method = relay_request.method

    header = {
        "Authorization": f"token {relay_request.oauth_token}",
    }

    if method == "GET":
        r = requests.get(url, headers=header)
    elif method == "POST":
        r = requests.post(url, headers=header)

    return r
   


