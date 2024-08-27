import streamlit as st
import time

from modules.settings.page import set_page_config, make_sidebar
from modules.settings.style import style_global
from modules.auth.api_auth import validate_token, get_user_info
from modules.security.encryption import str_to_asterisk
from modules.quiz.api_quiz import get_quiz, translate_quiz
from modules.quiz.streamlit_quiz import async_translation_interface, async_generation_interface, open_openaiapikey_modal, open_settings_modal

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
if "quiz_ready" not in st.session_state:
    st.session_state["quiz_ready"] = False
if "show_form" not in st.session_state:
    st.session_state["show_form"] = False
#redirect
if not st.session_state["auth_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")
st.session_state["token_status"] = validate_token(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])["status"]
if not st.session_state["token_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")

#settings
#page
set_page_config(auth_status=st.session_state["auth_status"],
                layout="wide")
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()
##############################################################################
#custom style
with open('/app/src/modules/quiz/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

#func
def reset_conversation():
  #message 초기화
  st.session_state["quiz_messages"] = [st.session_state["quiz_messages"][0]]
  ##st.session_state.chat_history = None

#main

col_1, col_2 = st.columns([1,1])
with col_1:
    st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 한국어 퀴즈 생성 </div>""", unsafe_allow_html=True)
with col_2:
    col_2_1, col_2_2, col_2_3 = st.columns([8,1,1])
    with col_2_2:
        if st.button(":material/account_circle:",key="df", use_container_width=False):
            st.switch_page("pages/my_profile.py")
    with col_2_3:     
        if st.button(":material/logout:",key="asdf", use_container_width=False):
            st.session_state = {}
            st.switch_page("main.py")
st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)

st.markdown("")
username = st.session_state["user_info"]["username"]

col1, col2 = st.columns((3,1), gap="small")

with col1:
    async_generation_interface()

    but1, but2, but3 = st.columns((1,1,1), gap="small")
    with but1:
        key_placeholder = st.container()
        if not st.session_state["key_status"]==True:
            if key_placeholder.button("OpenAI API KEY", type="primary", use_container_width=True, key="openai_api_key_button"):
                open_openaiapikey_modal()
        else:
            if key_placeholder.button("OpenAI API KEY", type="secondary", use_container_width=True, key="openai_api_key_2_button"):
                open_openaiapikey_modal(old_key=st.session_state["openai_api_key"])
    with but2:
        quiz_gen_placeholder = st.container()
        if not st.session_state["key_status"]==True:
            quiz_gen_placeholder.button("퀴즈 생성", type="primary", disabled=True, use_container_width=True)
        else:
            if quiz_gen_placeholder.button("퀴즈 생성", type="primary", use_container_width=True):
                open_settings_modal()

    with but3:
        quiz_del_placeholder = st.container()
        quiz_del_placeholder.button('대화 삭제', on_click=reset_conversation, use_container_width=True)   

    st.markdown("")

with col2:

    async_translation_interface()

    




