import requests
import dotenv
import os

dotenv.load_dotenv()


token = os.getenv('GITHUB_TOKEN')

headers = {
    "Authorization": f"token {token}",
}

r = requests.get("https://api.github.com/user", headers=headers)

data_dict = r.content.decode("utf-8")

# data = request.username, request.email, request.password, request.phone, request.display_name, request.github_oauth_token

username = data_dict['login']
email = data_dict['email']
phone = "phone"
display_name = data_dict['name']
github_oauth_token = data_dict['id']
