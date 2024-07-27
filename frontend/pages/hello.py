import streamlit as st
from time import sleep

from modules.settings.style import style_global
from modules.settings.page import set_page_config_sidebar_expanded, make_sidebar
from modules.auth.api_auth import validate_token

#settings
#page
set_page_config_sidebar_expanded()
#style
style_global()
#sidebar
make_sidebar()



#redirect
if not st.session_state["auth_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")
st.session_state["token_status"] = validate_token(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])["status"]
if not st.session_state["token_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")

"""
#sidebar
with st.sidebar:
    if st.button("로그아웃", use_container_width=False):
        st.session_state = {}
        st.switch_page("main.py")
"""
#main
if st.session_state["auth_status"] == True and st.session_state["token_status"] == True:
    st.subheader("👋 Hello", anchor=False)
    st.markdown(" ")





else:
    st.switch_page("main.py")

