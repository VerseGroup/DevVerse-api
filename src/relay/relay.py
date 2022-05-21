# imports
import base_models

# utils
from src.relay.utils import get_url

def relay(relay_request):
    url = get_url(relay_request.endpoint)
    data = relay_request.data
    method = relay_request.method

    if method == "GET":
        resp = base_models.get(url, json=data)
    elif method == "POST":
        resp = base_models.post(url, json=data)

    return resp.content.decode("utf-8")

