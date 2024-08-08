############################################################################
#경기도 데이터 분석 (경기일자리재단)
############################################################################

import streamlit as st

from modules.settings.page import set_page_config, make_sidebar
from modules.settings.style import style_global
from modules.auth.api_auth import validate_token, get_user_info

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
set_page_config(st.session_state["auth_status"],
                layout="wide") #default
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()

############################################################################

#main
col1, col2, col3 = st.columns((1,8,1), gap="large")
with col2:
    st.markdown("")
    st.subheader("🚀 경기도 데이터 분석", anchor=False)
    st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)




