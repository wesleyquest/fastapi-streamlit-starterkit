import streamlit as st
from modules.settings.style import style_global
from modules.settings.page import set_page_config, make_sidebar
from modules.auth.api_auth import validate_token, get_user_info
#custom_modules
from modules.glossary_htc.custom_func import load_data, make_glossary_terms, split_frame
import math
import warnings
warnings.filterwarnings('ignore')

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

#page settings
#page
set_page_config(auth_status=st.session_state["auth_status"],
                layout="wide")
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()
##############################################################################
#custom style
st.markdown("")
#main
##title
col_1, col_2 = st.columns([1,1])
with col_1:
    st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 용어사전 </div>""", unsafe_allow_html=True)
with col_2:
    col_2_1, col_2_2, col_2_3 = st.columns([8,1,1])
    with col_2_2:
        if st.button(":material/account_circle:",key="df", use_container_width=False):
            st.switch_page("pages/my_profile.py")
    with col_2_3:     
        if st.button(":material/logout:",key="asdf", use_container_width=False):
            st.session_state = {}
            st.switch_page("main.py")
st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
st.markdown("")

##content
###load data (from csv)
df_0 = load_data()
df_0 = make_glossary_terms(df_0)

top_menu = st.columns((5,2,1,2))
with top_menu[0]:
    view_radio = st.radio("보기", options=["전체", "PLANT", "UNIT", "EQP", "SUB_EQP", "OPER"], horizontal=1, index=0)
if view_radio == "PLANT":
    df_1 = df_0[df_0["CLASS"]=="PLANT"]
elif view_radio == "UNIT":
    df_1 = df_0[df_0["CLASS"]=="UNIT"]
elif view_radio == "EQP":
    df_1 = df_0[df_0["CLASS"]=="EQP"]
elif view_radio == "SUB_EQP":
    df_1 = df_0[df_0["CLASS"]=="SUB_EQP"]
elif view_radio == "OPER":
    df_1 = df_0[df_0["CLASS"]=="OPER"]
else:
    df_1 = df_0

with top_menu[2]:
    filter_selectbox = st.selectbox("코드 필터", options=["PLANT", "UNIT", "EQP", "SUB_EQP", "OPER"])

with top_menu[3]:
    filter_text_input = st.text_input("", "", placeholder="코드값을 입력하세요")
    if filter_text_input == "":
        df_1 = df_1
    else:
        if (filter_selectbox == "PLANT"):
            #df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[0] == filter_text_input]
            df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[0].str.contains(filter_text_input)==True]
        elif (filter_selectbox == "UNIT"):
            #df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[1] == filter_text_input]
            df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[1].str.contains(filter_text_input)==True]
        elif (filter_selectbox == "EQP"):
            #df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[2] == filter_text_input]
            df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[2].str.contains(filter_text_input)==True]
        elif (filter_selectbox == "SUB_EQP"):
            #df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[3] == filter_text_input]
            df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[3].str.contains(filter_text_input)==True]
        else: #OPER
            #df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[4] == filter_text_input]
            df_1 = df_1[df_1["HIERARCHY"].str.split(" > ").str[4].str.contains(filter_text_input)==True]

pagination = st.container()

bottom_menu = st.columns((4, 1, 1))
with bottom_menu[2]:
    batch_size = st.selectbox("Page Size", options=[25, 50, 100])
with bottom_menu[1]:
    total_pages = (
        #int(len(df_1) / batch_size) if int(len(df_1) / batch_size) > 0 else 1
        math.ceil(len(df_1) / batch_size) if int(len(df_1) / batch_size) > 0 else 1
    )
    current_page = st.number_input(
        "Page", min_value=1, max_value=total_pages, step=1
    )
    length = len(df_1)
with bottom_menu[0]:
    st.markdown(f"Page **{current_page}** of **{total_pages}** (Total : **{length}** rows)")

if len(df_1) > 0:
    df_1 = df_1.reset_index(drop=True)
    df_1.index = df_1.index+1
    pages = split_frame(df_1, batch_size)
    pagination.dataframe(data=pages[current_page - 1], 
                         use_container_width=True, 
                         column_config={
                             "CODE": st.column_config.Column(label="코드", width="small"),
                             "CLASS": st.column_config.Column(label="항목", width="small"),
                             "HIERARCHY": st.column_config.Column(label="카테고리", width="large"),
                             "DESC": st.column_config.Column(label="설명", width="large"),
                             "TYPE": st.column_config.Column(label="타입", width="small"),
                             "DATA_TYPE": st.column_config.Column(label="데이터 타입", width="small"),
                         },
                         height=500)
else:
    pagination.dataframe(data=df_1, use_container_width=True)


