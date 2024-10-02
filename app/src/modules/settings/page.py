import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from st_pages import hide_pages
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")


import base64

account_img_path = r'/app/src/images/account.png'
logout_img_path = r'/app/src/images/logout.png'
description_img_path = r'/app/src/images/description.png'
with open(account_img_path, "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode('utf-8')
with open(logout_img_path, "rb") as image_file:
    logout_img = base64.b64encode(image_file.read()).decode('utf-8')
with open(description_img_path, "rb") as image_file:
    description_img = base64.b64encode(image_file.read()).decode('utf-8')


#page config
#config
def set_page_config(auth_status, layout):
    if auth_status:
        st.set_page_config(
            page_title=APP_NAME,
            page_icon="📊",
            #layout="centered",
            initial_sidebar_state="auto",
            layout = layout,
            #menu_items={
            #    'Get Help': 'https://www.extremelycoolapp.com/help',
            #    'Report a bug': "https://www.extremelycoolapp.com/bug",
            #    'About': "# This is a header. This is an *extremely* cool app!"
            #}
        )
    else:
        st.set_page_config(
            page_title=APP_NAME,
            page_icon="📊",
            initial_sidebar_state="collapsed",
            layout=layout,
        )  

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar(auth_status, user_info):
    with st.sidebar:
        #st.markdown("<div style='text-align: center;'> 회사 로고 </div>", unsafe_allow_html=True)
        st.logo("/app/src/images/logo_wesleyquest.png", link="http://wesleyquest.com")
        st.markdown(f"<div style='text-align:center;font-size:20px;'><b> {APP_NAME} </b></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;font-size:16px;color:grey;'>{APP_VERSION}</div>", unsafe_allow_html=True)
        st.markdown("")
        #st.markdown("")
        
        if auth_status == True:
            with stylable_container(
                key="profile_popover",
                css_styles="""
                button {
                    color:white;
                    background-color:none;
                    border-color:#3D52A0;
                    text-align:left;
                }
                """
            ):

                with st.popover(f""":gray[**{user_info["username"]}**]  
                            :gray[{user_info["email"]}]""", use_container_width=True):
                    if st.button(":material/account_circle:&nbsp;&nbsp;나의 정보 (My Profile)", use_container_width=True):
                        profile_modal()
                        #st.switch_page("pages/my_profile.py")     
                    if st.button(":material/account_circle:&nbsp;&nbsp;나의 API KEY 정보 (My API Key)", use_container_width=True):
                        if not st.session_state["key_status"]==True:
                            open_openaiapikey_modal()
                        else:
                            open_openaiapikey_modal(old_key=st.session_state["openai_api_key"])
                    if st.button(":material/logout:&nbsp;&nbsp;로그 아웃 (Log Out)", use_container_width=True):
                        logout()    
            
            #st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
            with stylable_container(
                key="menu_expander",
                css_styles="""
                [data-testid="stExpander"] details{
                border-style:none;
                }
                """
            ):
                with st.expander("**HOME**", expanded=True):
                    st.page_link("pages/hello.py", label="매뉴얼", icon=":material/home:")
                with st.expander("**APP**", expanded=True):
                    st.page_link("pages/quiz_generator.py", label="한국어 퀴즈 생성", icon=":material/space_dashboard:")
                    st.page_link("pages/gjf.py", label="경기도 데이터 분석", icon=":material/space_dashboard:")
                    st.page_link("pages/resource_monitoring.py", label="자원 모니터링 분석", icon=":material/space_dashboard:")
                    st.page_link("pages/osstem_RAG.py", label="RAG 기반 답변", icon=":material/space_dashboard:")
                    st.page_link("pages/glossary_htc.py", label="용어사전 (POCHTC)", icon=":material/space_dashboard:")
                    st.page_link("pages/production_plan_htc.py", label="생산계획 분석 (POCHTC)", icon=":material/space_dashboard:")
                    st.page_link("pages/data_extraction_htc.py", label="데이터 추출 (POCHTC)", icon=":material/space_dashboard:")
                with st.expander("**API Docs**", expanded=True):
                    st.page_link("pages/api_docs_auth.py", label="로그인 API", icon=":material/description:")
                    st.page_link("pages/api_docs_quiz_generate.py", label="한국어 퀴즈 생성 API", icon=":material/description:")
                    st.page_link("pages/api_docs_quiz_translate.py", label="한국어 퀴즈 번역 API", icon=":material/description:")
                    st.page_link("pages/api_docs_user.py", label="사용자 관리 API (관리자용)", icon=":material/description:")

        elif not auth_status == True:
            st.page_link("main.py", label="로그인")
            st.page_link("pages/signup.py", label="회원가입")

        elif get_current_page_name() != "main":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("main.py")

def logout():
    st.session_state = {}
    st.switch_page("main.py")





from modules.auth.api_auth import get_access_token, validate_token, update_my_profile, get_user_info
from modules.validation.form_validation import validate_username, validate_password
from modules.validation.key_validation import get_api_key_check

#modal
@st.dialog(" ", width="small")
def profile_modal():
    st.markdown("""<div style="text-align:center;font-weight:bold;padding-bottom:5px;"> 나의 정보 </div>""", unsafe_allow_html=True)
    my_profile_form_placeholder = st.container()
    myprofile_info_placeholder = st.container()
    with my_profile_form_placeholder.form("my_profile_form_modal"):
        email = st.text_input("이메일", value=st.session_state["user_info"]["email"], disabled=True)
        st.markdown(" ")
        username = st.text_input("사용자명", value=st.session_state["user_info"]["username"], max_chars=30)
        username_valid_placeholder = st.container()
        st.markdown(" ")
        st.markdown(" ")
        password = st.text_input("*변경하시려면 비밀번호를 입력하세요", placeholder="password", type="password", max_chars=30)
        password_valid_placeholder = st.container()
        st.markdown(" ")
        submitted = st.form_submit_button("&nbsp;&nbsp;저&nbsp;&nbsp;장&nbsp;&nbsp;", type="primary", use_container_width=False)
        if submitted:
            #redirect
            if not st.session_state["auth_status"]==True:
                st.session_state = {}
                st.switch_page("main.py")
            st.session_state["token_status"] = validate_token(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])["status"]
            if not st.session_state["token_status"]==True:
                st.session_state = {}
                st.switch_page("main.py")
            #form validate
            valid = False
            if validate_username(username):
                if validate_password(password):
                    if get_access_token(st.session_state["user_info"]["email"], password)["status"]: #토큰은 받지 않지만 email, password 유효성 검증
                        valid=True
                    else:
                        myprofile_info_placeholder.error("비밀번호를 다시 입력하세요")
                else:
                    password_valid_placeholder.markdown(":red[비밀번호를 4자리 이상 입력하세요]")
            else:
                username_valid_placeholder.markdown(":red[사용자명을 4자리 이상 입력하세요]")

            if valid == True:
                #api
                data = update_my_profile(token_type = st.session_state["token_type"] ,
                                            access_token = st.session_state["access_token"],
                                            email = st.session_state["user_info"]["email"],
                                            username = username,
                                            password = password)
                
                if data["status"]:
                    myprofile_info_placeholder.info("성공적으로 변경되었습니다")
                    sleep(1)
                    st.rerun()
                else:
                    myprofile_info_placeholder.error(data["detail"])
    if st.button("&nbsp;&nbsp;닫&nbsp;&nbsp;기&nbsp;&nbsp;", type="secondary", use_container_width=False):
        st.rerun()
                        
#modal
@st.dialog(" ", width="small")
def open_openaiapikey_modal(old_key=None):
    if old_key:
        value = old_key
    else:
        value = None
    openai_api_key = st.text_input("OpenAI API KEY", value=value, key="chatbot_api_key", type="password")
    "[OpenAI API key 알아보기] (https://platform.openai.com/account/api-keys)"
    key_message_placeholder = st.container()
    st.markdown(" ")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("적용", type="primary", use_container_width=True, key="modal_openaiapikey_button"):
            api_key_value = get_api_key_check(
                token_type = st.session_state["token_type"], 
                access_token = st.session_state["access_token"],
                openai_api_key = openai_api_key
            )
            # key_message_placeholder.markdown(api_key_value)
            
            if api_key_value['results'] == "OPENAI_API_KEY is valid":
                st.session_state["key_status"] = True
                st.session_state["openai_api_key"] = openai_api_key
                st.rerun()
            else:
                key_message_placeholder.error(api_key_value["results"])

            # if validate_openai_api_key(openai_api_key):
            #     st.session_state["key_status"] = True
            #     st.session_state["openai_api_key"] = openai_api_key
            #     st.rerun()
            # else:
            #     key_message_placeholder.error("OpenAI API KEY를 정확히 입력하세요")
    with col2:
        if st.button("닫기", type="secondary", use_container_width=True):
            st.rerun()