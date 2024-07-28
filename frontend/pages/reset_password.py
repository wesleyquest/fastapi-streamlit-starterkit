import streamlit as st
from time import sleep

from modules.settings.style import style_global
from modules.settings.page import set_page_config, make_sidebar

#var
if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = None
if "token_status" not in st.session_state:
    st.session_state["token_status"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

#settings
#page
set_page_config(st.session_state["auth_status"])
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()

#main
st.markdown("")
st.markdown("<div style='text-align:center;font-size:30px;'><b>Reset password</b></div>", unsafe_allow_html=True)
st.markdown("")
st.markdown("<div style='text-align:center;font-size:20px;'><b>비밀번호를 재설정하세요</b></div>", unsafe_allow_html=True)
st.markdown("")
signup_info_placeholder = st.container()
with st.form("reset_password_form"):
    st.markdown(" ")
    password = st.text_input("*신규 비밀번호 (New password)", placeholder="비밀번호를 입력하세요 (4자리 이상)", type="password", max_chars=30)
    password_valid_placeholder = st.container()
    st.markdown(" ")
    password_re = st.text_input("*신규 비밀번호 확인 (Confirm new password)", placeholder="비밀번호를 다시 입력하세요", type="password", max_chars=30)
    password_re_valid_placeholder = st.container()
    st.markdown(" ")
    submitted = st.form_submit_button("비밀번호 재설정하기", type="primary", use_container_width=True)
    if submitted:
        #form validate
        from modules.validation.form_validation import (validate_password, validate_password_re)
        valid = False
        if validate_password(password):
            if validate_password_re(password_re, password):
                valid=True
            else:
                password_re_valid_placeholder.markdown(":red[비밀번호를 동일하게 입력하세요]")
        else:
            password_valid_placeholder.markdown(":red[비밀번호를 4자리 이상 입력하세요]")

        #api
        if valid==True:
                st.switch_page("main.py")
        else:
            st.switch_page("main.py")

if st.button("로그인 페이지로 돌아가기", use_container_width=True):
    st.switch_page("main.py")
