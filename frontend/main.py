import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages, Section, add_indentation
from time import sleep

from modules.custom.style import style_global
from modules.custom.style import set_page_config_sidebar_collapsed, set_page_config_sidebar_expanded
from modules.custom.style import show_pages_auth_false, show_pages_auth_true


#var
if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = None

#main
set_page_config_sidebar_collapsed()
style_global()
show_pages_auth_false()

st.markdown(" ")
with st.form("login_form"):
    st.markdown(" ")
    email = st.text_input("이메일", placeholder="Email")
    password = st.text_input("비밀번호", placeholder="Password", type="password")
    st.markdown(" ")
    submitted = st.form_submit_button("로그인", type="primary", use_container_width=True)
    if submitted:
        from modules.auth.api_auth import get_access_token
        data = get_access_token(email=email, password=password)
        
        if data["access_token"]:
            st.session_state["auth_status"] = True
            st.session_state["access_token"] = data["access_token"]
            st.session_state["token_type"] = data["token_type"]

            sleep(0.5) 
            show_pages_auth_true()
            #st.rerun()
            st.switch_page("pages/welcome.py")
        else:
            st.session_state["auth_status"] = False

    st.markdown(" ")

if st.button("회원가입", use_container_width=True):
    st.switch_page("pages/signup.py")



    






