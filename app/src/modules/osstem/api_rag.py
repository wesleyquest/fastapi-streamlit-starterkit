import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_SERVER = os.getenv("API_SERVER")
API_PORT = os.getenv("API_PORT")
API_V1_STR = os.getenv("API_V1_STR")

# batch 퀴즈 생성 API 호출 함수
def get_batch_rag(
        token_type,
        access_token,
        openai_api_key,
        query
):
    response = requests.post(
        url=f"http://{API_SERVER}:{API_PORT}{API_V1_STR}/rag/batch_generation",
        headers = {'Authorization': f'{token_type} {access_token}'},
        json={
            "openai_api_key": openai_api_key,
            "query": query
        },
        timeout=60
    )
    
    data = response.json()
    if response.status_code == 200:    
        data["status"] = True
    else:
        data["status"] = False
        data["results"] = "요청을 처리할 수 없습니다. 다시 시도해 주세요."
    return data
