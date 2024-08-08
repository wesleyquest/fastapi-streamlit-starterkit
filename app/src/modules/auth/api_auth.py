import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_SERVER = os.getenv("API_SERVER")
API_PORT = os.getenv("API_PORT")
API_V1_STR = os.getenv("API_V1_STR")


def validate_token(token_type, access_token):
    try:
        response = requests.post(
            url=f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/auth/login/test-token",
            headers = {'Authorization': f'{token_type} {access_token}'},
            timeout=5
        )
        
        data = response.json()
        if response.status_code == 200:    
            data["status"] = True
        else:
            data["status"] = False
        return data

    except:
        return {
            "status": False,
            "detail": "요청을 처리할 수 없습니다. 다시 시도해 주세요."
        }


def get_user_info(token_type, access_token):
    """
    """
    try:
        response = requests.request(
            method="get",
            url = f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/users/me",
            headers = {'Authorization': f'{token_type} {access_token}'},
            timeout=5
        )

        data = response.json()
        if response.status_code == 200:    
            data["status"] = True
        else:
            data["status"] = False
        return data
    except:
        return {
            "status": False,
            "detail": "요청을 처리할 수 없습니다. 다시 시도해 주세요."
        }

def get_access_token(email, password):
    """
    return
    {
        "access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjE3MTY2MTAsInN1YiI6IjEifQ.onTsWDNJ_xxT9ZwbhBZj3AayAd42_3C5bBeH77eXTi4"
        "token_type":"bearer"
        "detail":"login success"
    }
    """
    try:
        response = requests.request(
            method="post",
            url= f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/auth/login/access-token",
            data={"username": email, "password": password},
            timeout=5
        )

        data = response.json()
        if response.status_code == 200:    
            data["status"] = True
        else:
            data["status"] = False
        return data
    except:
        return {
            "status": False,
            "detail": "요청을 처리할 수 없습니다. 다시 시도해 주세요."
        }

def create_user(email, username, password):
    try:
        response = requests.post(
            url=f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/users/signup",
            json={
                "email": email,
                "password": password,
                "username": username},
            timeout=5
        )

        data = response.json()
        if response.status_code == 200:    
            data["status"] = True
        else:
            data["status"] = False
        return data
    except:
        return {
            "status": False,
            "detail": "요청을 처리할 수 없습니다. 다시 시도해 주세요."
        }


def update_my_profile(token_type, access_token, email, username, password):
    try:
        response = requests.put(
            url=f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/users/me",
            headers = {'Authorization': f'{token_type} {access_token}'},
            json={
                "email": email,
                "password": password,
                "username": username},
            timeout=5
        )

        data = response.json()
        if response.status_code == 200:    
            data["status"] = True
        else:
            data["status"] = False
        return data
    except:
        return {
            "status": False,
            "detail": "요청을 처리할 수 없습니다. 다시 시도해 주세요."
        }


def send_forgot_password_email(email):
    try:
        response = requests.post(
            url=f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/auth/password-recovery/{email}",
            json="",
            timeout=5
        )

        data = response.json()
        if response.status_code == 200:    
            data["status"] = True
        else:
            data["status"] = False
        return data
    except:
        return {
            "status": False,
            "detail": "요청을 처리할 수 없습니다. 다시 시도해 주세요."
        }


def reset_password(reset_password_token, new_password):
    try:
        response = requests.post(
            url=f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/auth/reset-password",
            json={
                "token": reset_password_token,
                "new_password": new_password
            },
            timeout=5
        )

        data = response.json()
        if response.status_code == 200:    
            data["status"] = True
        else:
            data["status"] = False
        return data
    except:
        return {
            "status": False,
            "detail": "요청을 처리할 수 없습니다. 다시 시도해 주세요."
        }


