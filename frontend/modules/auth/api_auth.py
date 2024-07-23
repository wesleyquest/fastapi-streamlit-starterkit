import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_SERVER = os.getenv("BACKEND_SERVER")


def get_user_info(token_type, access_token):
    """
    """
    response = requests.request(
        method="get",
        url = f"http://{BACKEND_SERVER}:8000/api/v1/users/me",
        headers = {'Authorization': f'{token_type} {access_token}'},
        timeout=5
    )

    data = response.json()

    return data


def get_access_token(username, password):
    """
    return
    {
        "access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjE3MTY2MTAsInN1YiI6IjEifQ.onTsWDNJ_xxT9ZwbhBZj3AayAd42_3C5bBeH77eXTi4"
        "token_type":"bearer"
        "detail":"login success"
    }
    """

    response = requests.request(
        method="post",
        url= f"http://{BACKEND_SERVER}:8000/api/v1/auth/login/access-token",
        data={"username": username, "password": password},
        timeout=5
    )

    data = response.json()

    if not "access_token" in data.keys():
        data["access_token"] = None
        data["token_type"] = None
        data["detail"] = data["detail"]

    else:
        data["detail"] = "login success"

    return data




