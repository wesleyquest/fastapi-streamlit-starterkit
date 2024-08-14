import streamlit as st
import yaml
import os
from dotenv import load_dotenv

from modules.settings.style import style_global
from modules.settings.page import set_page_config, make_sidebar
from modules.auth.api_auth import validate_token, get_user_info

load_dotenv()
SERVER_HOST = os.getenv("SERVER_HOST")
#@st.cache_data
with open("/app/src/docs/quiz/api_docs_generation.yml") as f:
    docs = yaml.load(f, Loader=yaml.FullLoader)

#var
if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = None
if "token_status" not in st.session_state:
    st.session_state["token_status"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "key_status" not in st.session_state:
    st.session_state["key_status"] = None
if st.session_state["auth_status"]==True:
    st.session_state["user_info"] = get_user_info(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])
#redirect
if not st.session_state["auth_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")
st.session_state["token_status"] = validate_token(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])["status"]
if not st.session_state["token_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")

#page settings
#page
set_page_config(auth_status=st.session_state["auth_status"],
                layout="wide")

#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()

#main
col1, col2, col3 = st.columns((1,8,1), gap="small")
with col2:
    st.markdown("")
    st.subheader("📑 한국어 퀴즈 생성 API", anchor=False)
    st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h4>한국어 퀴즈 생성</h4>", unsafe_allow_html=True)
        st.markdown("<h5>기본 정보</h5>", unsafe_allow_html=True)
        st.markdown(f"""{docs["summary"]}""", unsafe_allow_html=True)
        st.markdown(f"""
                    <table style="width:100%; height:100%;">
                    <tr>
                        <td style="width:25%; background-color:#F0F2F6; font-weight:bold;"> 메서드 </td>
                        <td style="width:55%; background-color:#F0F2F6; font-weight:bold;"> URL </td>
                        <td style="width:20%; background-color:#F0F2F6; font-weight:bold;"> 인증 방식 </td>
                    </tr>
                    <tr>
                        <td> {docs["method"]} </td>
                        <td> {SERVER_HOST}{docs["url"]} </td>
                        <td> {docs["auth_method"]} </td>
                    </tr>
                    </table>
                    """
                    , unsafe_allow_html=True)
        st.markdown("")
        st.markdown("<h5>요청</h5>", unsafe_allow_html=True)
        st.markdown("**헤더**")
        st.markdown(f"""
                    <table style="width:100%; height:100%;">
                    <tr>
                        <td style="width:25%; background-color:#F0F2F6; font-weight:bold;"> 이름 </td>
                        <td style="width:55%; background-color:#F0F2F6; font-weight:bold;"> 설명 </td>
                        <td style="width:20%; background-color:#F0F2F6; font-weight:bold;"> 필수 </td>
                    </tr>
                    <tr>
                        <td> {docs["request"]["headers"]["key_1"]["name"]} </td>
                        <td> {docs["request"]["headers"]["key_1"]["desc"]} </td>
                        <td> {docs["request"]["headers"]["key_1"]["required"]} </td>
                    </tr>
                    </table>
                    """
                    , unsafe_allow_html=True)
        st.markdown("**본문**")
        st.markdown(f"""
                    <table style="width:100%; height:100%;">
                    <tr>
                        <td style="width:20%; background-color:#F0F2F6; font-weight:bold;"> 이름 </td>
                        <td style="width:15%; background-color:#F0F2F6; font-weight:bold;"> 타입 </td>
                        <td style="width:50%; background-color:#F0F2F6; font-weight:bold;"> 설명 </td>
                        <td style="width:15%; background-color:#F0F2F6; font-weight:bold;"> 필수 </td>
                    </tr>
                    <tr>
                        <td> {docs["request"]["body"]["key_1"]["name"]} </td>
                        <td> {docs["request"]["body"]["key_1"]["type"]} </td>
                        <td> {docs["request"]["body"]["key_1"]["desc"]} </td>
                        <td> {docs["request"]["body"]["key_1"]["required"]} </td>
                    </tr>
                    <tr>
                        <td> {docs["request"]["body"]["key_2"]["name"]} </td>
                        <td> {docs["request"]["body"]["key_2"]["type"]} </td>
                        <td> {docs["request"]["body"]["key_2"]["desc"]} </td>
                        <td> {docs["request"]["body"]["key_2"]["required"]} </td>
                    </tr>
                    <tr>
                        <td> {docs["request"]["body"]["key_3"]["name"]} </td>
                        <td> {docs["request"]["body"]["key_3"]["type"]} </td>
                        <td> {docs["request"]["body"]["key_3"]["desc"]} </td>
                        <td> {docs["request"]["body"]["key_3"]["required"]} </td>
                    </tr>
                    <tr>
                        <td> {docs["request"]["body"]["key_4"]["name"]} </td>
                        <td> {docs["request"]["body"]["key_4"]["type"]} </td>
                        <td> {docs["request"]["body"]["key_4"]["desc"]} </td>
                        <td> {docs["request"]["body"]["key_4"]["required"]} </td>
                    </tr>
                    <tr>
                        <td> {docs["request"]["body"]["key_5"]["name"]} </td>
                        <td> {docs["request"]["body"]["key_5"]["type"]} </td>
                        <td> {docs["request"]["body"]["key_5"]["desc"]} </td>
                        <td> {docs["request"]["body"]["key_5"]["required"]} </td>
                    </tr>
                    </table>
                    """
                    , unsafe_allow_html=True)
        st.markdown("")
        st.markdown("<h5>응답</h5>", unsafe_allow_html=True)
        st.markdown("**본문**")
        st.markdown(f"""
                    <table style="width:100%; height:100%;">
                    <tr>
                        <td style="width:20%; background-color:#F0F2F6; font-weight:bold;"> 이름 </td>
                        <td style="width:15%; background-color:#F0F2F6; font-weight:bold;"> 타입 </td>
                        <td style="width:50%; background-color:#F0F2F6; font-weight:bold;"> 설명 </td>
                        <td style="width:15%; background-color:#F0F2F6; font-weight:bold;"> 필수 </td>
                    </tr>
                    <tr>
                        <td> {docs["response"]["body"]["key_1"]["name"]} </td>
                        <td> {docs["response"]["body"]["key_1"]["type"]} </td>
                        <td> {docs["response"]["body"]["key_1"]["desc"]} </td>
                        <td> {docs["response"]["body"]["key_1"]["required"]} </td>
                    </tr>
                    </table>
                    """
                    , unsafe_allow_html=True)
        st.markdown("")
        st.markdown("<h5>예제</h5>", unsafe_allow_html=True)
        st.markdown("**요청**")
        tab1, tab2 = st.tabs(["Shell", "Python"])
        code_shellSession = """
        (수정)
        """
        code_python = """
        import requests

        try:
            response = requests.request(
                method="post",
                url= "http://211.218.17.10/api/v1/quiz/generation",
                headers = {
                    "Content-type": "application/json",
                    "Authorization": "bearer eyJh...XYOw" 
                },
                json={
                    "openai_api_key": ${OPENAI_API_KEY},
                    "document": ${DOCUMENT},
                    "quiz_content": ${QUIZ_CONTENT},
                    "quiz_type": ${QUIZ_TYPE},
                    "number": ${NUMBER}
                }
            )
            print(response.status_code)
            print(response.json())

        except Exception as err:
            print(err)
        """
        with tab1:
            st.code(code_shellSession)  
        with tab2:
            st.code(code_python, language="python")  
        st.markdown("")
        st.markdown("**응답**")
        tab1, tab2 = st.tabs(["성공", "실패"])
        code_success="""
        {
            "results": "아래와 같이 퀴즈를 생성했어요. ..."
        }
        """
        code_fail="""
        {
            'detail': [
                {
                    'type': 'list_type',
                    'loc': ['body', 'quiz_type'],
                    'msg': 'Input should be a valid list',
                    'input': 'adsf'
                }
            ]
        }
        """
        with tab1:
            st.code(code_success, language="python")   
        with tab2:
            st.code(code_fail, language="python")  


st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
