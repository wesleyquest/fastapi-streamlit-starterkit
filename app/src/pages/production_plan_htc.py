import streamlit as st
import pandas as pd
from modules.settings.style import style_global
from modules.settings.page import set_page_config, make_sidebar
from modules.auth.api_auth import validate_token, get_user_info
#custom_modules
from modules.production_plan_htc.extract_transform import load_data, create_df_fmf_main, create_df_fmf_quality
from modules.production_plan_htc.create_chart import create_gantt_chart, create_quality_chart
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
    st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 생산계획 분석 </div>""", unsafe_allow_html=True)
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
fmf_schedule_df, grade_info_df = load_data()
df_fmf_main = create_df_fmf_main(fmf_schedule_df, grade_info_df)
df_fmf_quality = create_df_fmf_quality(df_fmf_main)
range_x=[pd.Timestamp(min(df_fmf_main["Start"]).strftime('%Y-%m-%d')),
         pd.Timestamp((max(df_fmf_main["End"]) + pd.Timedelta(1,"d")).strftime('%Y-%m-%d'))]
fig_1 = create_gantt_chart(df_fmf_main)
fig_2 = create_quality_chart(df_fmf_quality, range_x)

gantt_chart_container = st.container(border=True)
quality_chart_container = st.container(border=True)

with gantt_chart_container:
    st.markdown("""<div style="font-size:20px;font-weight:bold;font-family:'Gothic A1';"> 생산계획 간트차트 </div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_1, use_container_width=True)
with quality_chart_container:
    st.markdown("""<div style="font-size:20px;font-weight:bold;font-family:'Gothic A1';"> 품질점검 계획표 </div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_2, use_container_width=True)

