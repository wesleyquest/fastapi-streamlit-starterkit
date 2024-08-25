import streamlit as st
from time import sleep

from modules.settings.page import set_page_config, make_sidebar
from modules.settings.style import style_global
from modules.auth.api_auth import get_access_token, validate_token, update_my_profile, get_user_info
from modules.validation.form_validation import validate_username, validate_password

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
                layout="centered")
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()
        
#modal
@st.dialog(" ", width="small")
def open_change_myprofile_modal(token_type, access_token, email, username, password):
    st.markdown("My Profile 정보를 변경하시겠습니까?")

    col1, col2 = st.columns(2)


    if col1.button("변경", type="primary", use_container_width=True, key="modal_change_myprofile_button"):
        #api
        data = update_my_profile(token_type = token_type ,
                                    access_token = access_token,
                                    email = email,
                                    username = username,
                                    password = password)
        if data["status"]:
            sleep(0.5)
            st.rerun()
        else:
            myprofile_info_placeholder.error(data["detail"])
            st.rerun()

    if col2.button("취소", type="secondary", use_container_width=True):
        st.rerun()

##############################################################################
#custom style
st.markdown("")
#main
##title
col_1, col_2 = st.columns([1,1])
with col_1:
    st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 나의 정보 </div>""", unsafe_allow_html=True)
with col_2:
    col_2_1, col_2_2, col_2_3 = st.columns([6,2,2])
    with col_2_2:
        if st.button(":material/account_circle:",key="df", use_container_width=False):
            st.switch_page("pages/my_profile.py")
    with col_2_3:     
        if st.button(":material/logout:",key="asdf", use_container_width=False):
            st.session_state = {}
            st.switch_page("main.py")
st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
st.markdown("")
with st.container(border=True):
    tab1, tab2 = st.tabs(["프로필 보기", "프로필 변경"])
    with tab1:
        email = st.session_state["user_info"]["email"]
        username = st.session_state["user_info"]["username"]
        st.markdown(f"이메일  \n :gray-background[{email}]")
        if username:
            st.markdown(f"사용자명  \n :gray-background[{username}]")


    with tab2:
        myprofile_info_placeholder = st.container()
        with st.form("my_profile_form"):
            email = st.text_input("이메일", value=st.session_state["user_info"]["email"], disabled=True)
            st.markdown(" ")
            username = st.text_input("사용자명", value=st.session_state["user_info"]["username"], max_chars=30)
            username_valid_placeholder = st.container()
            st.markdown(" ")
            st.markdown(" ")
            password = st.text_input("*변경하시려면 비밀번호를 입력하세요", placeholder="password", type="password", max_chars=30)
            password_valid_placeholder = st.container()
            st.markdown(" ")
            submitted = st.form_submit_button("변경", type="primary", use_container_width=True)

            if submitted:
                #form validate
                valid = False
                if validate_username(username):
                    if validate_password(password):
                        if get_access_token(st.session_state["user_info"]["email"], password)["status"]: #토큰은 받지 않지만 email, password 유효성 검증
                            valid=True
                        else:
                            myprofile_info_placeholder.error("비밀번호를 확인하세요")
                    else:
                        password_valid_placeholder.markdown(":red[비밀번호를 4자리 이상 입력하세요]")
                else:
                    username_valid_placeholder.markdown(":red[사용자명을 4자리 이상 입력하세요]")

                if valid == True:
                    open_change_myprofile_modal(token_type=st.session_state["token_type"],
                                                access_token=st.session_state["access_token"],
                                                email=st.session_state["user_info"]["email"],
                                                password=password,
                                                username=username)






