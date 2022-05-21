# imports
import requests

# utils
from src.relay.utils import get_url

def relay(relay_request):
    url = get_url(relay_request.endpoint)
    data = relay_request.data
    method = relay_request.method

    if method == "GET":
        resp = requests.get(url, json=data)
    elif method == "POST":
        resp = requests.post(url, json=data)

    return resp.content.decode("utf-8")

