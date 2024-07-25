import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages, Section, add_indentation
from time import sleep

from modules.custom.style import style_global
from modules.custom.style import set_page_config_sidebar_collapsed
from modules.custom.style import show_pages_auth_false, show_pages_auth_true

set_page_config_sidebar_collapsed()
style_global()
show_pages_auth_false()

#var
if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = None

#main
st.markdown("")
with st.form("signup_form"):
    st.markdown("회원가입") #
    email = st.text_input("*이메일 아이디", placeholder="Email 주소를 입력하세요", max_chars=100)
    email_valid_placeholder = st.container()
    username = st.text_input("*사용자명", placeholder="사용자명을 입력하세요 (4자리 이상)", max_chars=30)
    username_valid_placeholder = st.container()
    password = st.text_input("*비밀번호", placeholder="비밀번호를 입력하세요 (4자리 이상)", type="password", max_chars=30)
    password_valid_placeholder = st.container()
    password_re = st.text_input("*비밀번호 확인", placeholder="비밀번호를 다시 입력하세요", type="password", max_chars=30)
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
                st.info("회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.")
                sleep(0.5)
                st.switch_page("main.py")
            else:
                st.error(data["detail"])

if st.button("로그인 페이지로 돌아가기", use_container_width=True):
    st.switch_page("main.py")




