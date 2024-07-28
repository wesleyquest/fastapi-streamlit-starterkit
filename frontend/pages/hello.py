import streamlit as st
from time import sleep

from modules.settings.style import style_global
from modules.settings.page import set_page_config, make_sidebar
from modules.auth.api_auth import validate_token

#var
if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = None
if "token_status" not in st.session_state:
    st.session_state["token_status"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

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
set_page_config(st.session_state["auth_status"])
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()

#main
st.markdown("")
st.subheader("👋 Hello", anchor=False)


