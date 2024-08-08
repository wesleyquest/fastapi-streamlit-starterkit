import streamlit as st
from time import sleep

from modules.settings.style import style_global
from modules.settings.page import set_page_config, make_sidebar
from modules.auth.api_auth import send_forgot_password_email
from modules.validation.form_validation import validate_email

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

#modal
@st.dialog(" ", width="small")
def open_send_forgot_password_mail_modal(email, data):
    if data["status"] == True:
        st.markdown("")
        st.markdown(f"""<div style='text-align:center;font-size:20px;'><b>{data["detail"]}</b></div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("<div style='text-align:center;'>메일을 확인하시고 비밀번호를 재설정 해주세요</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;'>{email}</div>", unsafe_allow_html=True)
    else:
        st.markdown("")
        st.markdown(f"""<div style='text-align:center;font-size:20px;'><b>{data["detail"]}</b></div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("<div style='text-align:center;'>입력하신 이메일 정보를 다시 확인해 주세요</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;'>{email}</div>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    if st.button("확인", type="secondary", use_container_width=True, key="modal_change_myprofile_button"):
        st.rerun()


st.markdown("")
st.markdown("<div style='text-align:center;font-size:30px;'><b>Forgot your password?</b></div>", unsafe_allow_html=True)
st.markdown("")
st.markdown("<div style='text-align:center;font-size:20px;'><b>비밀번호를 잊어버리셨나요?</b></div>", unsafe_allow_html=True)
st.markdown("")
st.markdown("<div style='text-align:center;'>가입했던 이메일을 입력해주세요</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;'>비밀번호 재설정 메일을 보내드립니다</div>", unsafe_allow_html=True)
st.markdown("")
with st.form("forgot_password_form"):   
    st.markdown(" ")
    email = st.text_input("*이메일 (Email address)", placeholder="Email 주소를 입력하세요", max_chars=100)
    email_valid_placeholder = st.container()
    st.markdown(" ")

    submitted = st.form_submit_button("이메일 보내기", type="primary", use_container_width=True)
    
    valid=False
    if submitted:
        if validate_email(email):
            valid=True
        else:
            email_valid_placeholder.markdown(":red[이메일 형식을 확인하세요]")

    #api
    if valid==True:
        data = send_forgot_password_email(email)
        open_send_forgot_password_mail_modal(email, data)

if st.button("로그인 페이지로 돌아가기", use_container_width=True):
    st.switch_page("main.py")
