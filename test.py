import base_models


site_session = base_models.Session()
url = "https://github.com/login/oauth/authorize"
data = {
    "client_id": "0dbbdc9a9550b94c98c2"
}
resp = site_session.get(url, json=data)

print(resp.content.decode("utf-8"))


