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
set_page_config(auth_status=st.session_state["auth_status"],
                layout="centered")
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()



#main
st.markdown("")
st.markdown("<div style='text-align:center;font-size:30px;'><b>Sign up to Dashboard</b></div>", unsafe_allow_html=True)
st.markdown("")
st.markdown("<div style='text-align:center;font-size:20px;'><b>스타터킷 대시보드 회원가입</b></div>", unsafe_allow_html=True)
st.markdown("")
signup_info_placeholder = st.container()
with st.form("signup_form"):
    st.markdown(" ")
    email = st.text_input("*이메일 (Email address)", placeholder="Email 주소를 입력하세요", max_chars=100)
    email_valid_placeholder = st.container()
    st.markdown(" ")
    username = st.text_input("*사용자명 (Username)", placeholder="사용자명을 입력하세요 (4자리 이상)", max_chars=30)
    username_valid_placeholder = st.container()
    st.markdown(" ")
    password = st.text_input("*비밀번호 (Password)", placeholder="비밀번호를 입력하세요 (4자리 이상)", type="password", max_chars=30)
    password_valid_placeholder = st.container()
    st.markdown(" ")
    password_re = st.text_input("*비밀번호 확인 (Confirm Password)", placeholder="비밀번호를 다시 입력하세요", type="password", max_chars=30)
    password_re_valid_placeholder = st.container()
    st.markdown(" ")
    submitted = st.form_submit_button("회원가입", type="primary", use_container_width=True)
    if submitted:
        #form validate
        from modules.validation.form_validation import (
            validate_email, validate_username, validate_password, validate_password_re)
        valid = False
        if validate_email(email):
            if validate_username(username):
                if validate_password(password):
                    if validate_password_re(password_re, password):
                        valid=True
                    else:
                        password_re_valid_placeholder.markdown(":red[비밀번호를 동일하게 입력하세요]")
                else:
                    password_valid_placeholder.markdown(":red[비밀번호를 4자리 이상 입력하세요]")
            else:
                username_valid_placeholder.markdown(":red[사용자명을 4자리 이상 입력하세요]")
        else:
            email_valid_placeholder.markdown(":red[이메일 형식을 확인하세요]")

        #api
        if valid==True:
            from modules.auth.api_auth import create_user
            data = create_user(email=email, username=username, password=password)
            if data["status"]:
                signup_info_placeholder.info("회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.")
                sleep(0.5)
                st.switch_page("main.py")
            else:
                signup_info_placeholder.error(data["detail"])

if st.button("로그인 페이지로 돌아가기", use_container_width=True):
    st.switch_page("main.py")




