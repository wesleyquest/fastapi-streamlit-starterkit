import streamlit as st
from time import sleep

from modules.settings.style import style_global
from modules.settings.page import set_page_config, make_sidebar
from modules.auth.api_auth import reset_password

#query_params
if not st.query_params:
    st.markdown("")
    st.markdown("<div style='text-align:center;font-size:30px;'><b>Authentication failed</b></div>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("<div style='text-align:center;font-size:20px;'><b>인증이 실패했습니다</b></div>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("<div style='text-align:center;'>비밀번호 재설정을 다시 진행해 주세요</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'>로그인 페이지로 이동합니다</div>", unsafe_allow_html=True)
    sleep(3)
    st.switch_page("main.py")
else:
    st.session_state["reset_password_token"] = st.query_params["token"]

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

#modal
@st.dialog(" ", width="small")
def open_reset_password_modal(data):
    if data["status"] == True:
        st.markdown("")
        st.markdown("""<div style='text-align:center;font-size:20px;'><b>비밀번호를 변경하였습니다</b></div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("<div style='text-align:center;'>로그인을 진행해 주세요</div>", unsafe_allow_html=True)
    else:
        st.markdown("")
        st.markdown(f"""<div style='text-align:center;font-size:20px;'><b>인증이 실패했습니다</b></div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("<div style='text-align:center;'>비밀번호 재설정을 다시 진행해 주세요</div>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    if st.button("확인", type="secondary", use_container_width=True, key="modal_change_myprofile_button"):
        st.switch_page("main.py")


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
                data = reset_password(st.session_state["reset_password_token"], password)
                open_reset_password_modal(data)

if st.button("로그인 페이지로 돌아가기", use_container_width=True):
    st.switch_page("main.py")
