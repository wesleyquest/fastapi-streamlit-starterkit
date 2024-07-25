import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages, Section, add_indentation
from time import sleep

from modules.custom.style import style_global
from modules.custom.style import set_page_config_sidebar_expanded
from modules.custom.style import show_pages_auth_true, show_pages_auth_false


set_page_config_sidebar_expanded()
show_pages_auth_true()
style_global()

#validate token & redirect
if st.session_state["auth_status"]==True:
    from modules.auth.api_auth import validate_token
    data = validate_token(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])
    if not data["status"]:
        st.session_state = {}
        show_pages_auth_false()
        st.switch_page("main.py")
        

#var
if st.session_state["auth_status"]==True:
    from modules.auth.api_auth import get_user_info
    st.session_state["user_info"] = get_user_info(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])



st.title("My Profile", anchor=False)

#main
st.markdown("")
with st.form("my_profile_form"):
    st.markdown("내 프로필 정보") #
    email = st.text_input("*이메일 아이디", value=st.session_state["user_info"]["email"], max_chars=100)
    email_valid_placeholder = st.container()
    username = st.text_input("*사용자명", value=st.session_state["user_info"]["full_name"], max_chars=30)
    username_valid_placeholder = st.container()
    password = st.text_input("*비밀번호", placeholder="비밀번호를 입력하세요 (4자리 이상)", type="password", max_chars=30)
    password_valid_placeholder = st.container()
    st.markdown(" ")
    submitted = st.form_submit_button("변경", type="primary", use_container_width=True)

    if submitted:
        #form validate
        from modules.validation.form_validation import (
            validate_email, validate_username, validate_password, validate_password_re)
        valid = False
        if validate_email(email):
            if validate_username(username):
                if validate_password(password):
                    valid=True
                else:
                    password_valid_placeholder.markdown(":red[비밀번호를 4자리 이상 입력하세요]")
            else:
                username_valid_placeholder.markdown(":red[사용자명을 4자리 이상 입력하세요]")
        else:
            email_valid_placeholder.markdown(":red[이메일 형식을 확인하세요]")

        #api
        if valid==True:
            from modules.auth.api_auth import update_my_profile
            data = update_my_profile(token_type = st.session_state["token_type"] ,
                                     access_token = st.session_state["access_token"],
                                     email = email,
                                     username = username,
                                     password = password)
            if data["status"]:
                st.toast("내 프로필 정보가 번경되었습니다.")
                sleep(0.5)
                st.rerun()
            else:
                st.error(data["detail"])



