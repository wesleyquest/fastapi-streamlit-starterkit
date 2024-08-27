import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_SERVER = os.getenv("API_SERVER")
API_PORT = os.getenv("API_PORT")
API_V1_STR = os.getenv("API_V1_STR")

# def get_quiz(
#         token_type,
#         access_token,
#         openai_api_key,
#         document,
#         quiz_content,
#         quiz_type,
#         number
# ):
#     response = requests.post(
#         url=f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/quiz/generation",
#         headers = {'Authorization': f'{token_type} {access_token}'},
#         json={
#             "openai_api_key": openai_api_key,
#             "document": document,
#             "quiz_content": quiz_content,
#             "quiz_type": quiz_type,
#             "number": number
#         },
#         timeout=60
#     )
    
#     data = response.json()
#     if response.status_code == 200:    
#         data["status"] = True
#     else:
#         data["status"] = False
#         data["results"] = "요청을 처리할 수 없습니다. 다시 시도해 주세요."
#     return data

def get_quiz(
        token_type,
        access_token,
        openai_api_key,
        document,
        quiz_content,
        quiz_type,
        number
):
    try: 
        response = requests.post(
            url=f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/quiz/generation",
            headers = {'Authorization': f'{token_type} {access_token}',
                        #'Accept': 'text/event-stream'
            },
            json={
                "openai_api_key": openai_api_key,
                "document": document,
                "quiz_content": quiz_content,
                "quiz_type": quiz_type,
                "number": number
            },
            stream = True,
            timeout=60
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                yield line.decode('utf-8')
    except requests.exceptions.RequestException as e:
        yield f"Error: {str(e)}"
        


# def translate_quiz(
#         token_type,
#         access_token,
#         openai_api_key,
#         quiz,
#         language
# ):
#     response = requests.post(
#         url=f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/quiz/translation",
#         headers = {'Authorization': f'{token_type} {access_token}'},
#         json={
#             "openai_api_key": openai_api_key,
#             "quiz": quiz,
#             "language": language,
#         },
#         timeout=60
#     )
 
#     data = response.json()
#     if response.status_code == 200:    
#         data["status"] = True
#     else:
#         data["status"] = False
#         data["results"] = "요청을 처리할 수 없습니다. 다시 시도해 주세요."
#     return data

def translate_quiz(
        token_type,
        access_token,
        openai_api_key,
        quiz,
        language
):
    url = f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/quiz/translation"
    headers = {
        'Authorization': f'{token_type} {access_token}',
        #'Accept': 'text/event-stream'
    }
    data = {
        "openai_api_key": openai_api_key,
        "quiz": quiz,
        "language": language,
    }

    try:
        response = requests.post(url, headers=headers, json=data, stream=True, timeout=60)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

        for line in response.iter_lines():
            if line:
                yield line.decode('utf-8')
    except requests.exceptions.RequestException as e:
        yield f"Error: {str(e)}"