import streamlit as st
import pandas as pd
import numpy as np
import time

from modules.settings.page import set_page_config, make_sidebar
from modules.settings.style import style_global
from modules.auth.api_auth import validate_token, get_user_info
from modules.security.encryption import str_to_asterisk
#from modules.validation.key_validation import validate_openai_api_key
from modules.validation.form_validation import validate_text
#from modules.quiz.api_quiz import get_quiz

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
                layout="wide")
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()
##############################################################################
#custom style
with open('/app/src/modules/resource_monitoring/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

#main
##title
col_1, col_2 = st.columns([1,1])
with col_1:
    st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 자원 모니터링 분석 </div>""", unsafe_allow_html=True)
with col_2:
    col_2_1, col_2_2, col_2_3 = st.columns([8,1,1])
    with col_2_2:
        if st.button(":material/account_circle:",key="df", use_container_width=False):
            st.switch_page("pages/my_profile.py")
    with col_2_3:     
        if st.button(":material/logout:",key="asdf", use_container_width=False):
            st.session_state = {}
            st.switch_page("main.py")
#st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 자원 모니터링 분석 </div>""", unsafe_allow_html=True)
st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
st.markdown("")

##widget
col_widget_1, col_widget_2 = st.columns([1,1])
with col_widget_1:
    st.markdown("""<div style="font-size:18;font-weight:bold;font-family:'Gothic A1';">※ 기준 시점 : 2024년 8월 25일 오후 7시 54분 20초 </div>""", unsafe_allow_html=True)
    st.markdown("")

##dashboard header
col_1, col_2, col_3, col_4, col_5 = st.columns([1,1,1,1,1])
with col_1:
    with st.container(border=True):
        CPU_usage = "65 %"
        st.markdown(f"""<p class="header_text">CPU 사용률</p>
                    <p class="number_up">
                    {CPU_usage}
                    <span class="symbol_up"> ▲ </span>
                    </p>
                    """, unsafe_allow_html = True)

with col_2:
    with st.container(border=True):
        Mem_usage = "70 %"
        st.markdown(f"""<p class="header_text">Mem 사용률</p>
                    <p class="number_up">
                    {Mem_usage}
                    <span class="symbol_up"> ▲ </span>
                    </p>
                    """, unsafe_allow_html = True)

with col_3:
    with st.container(border=True):
        Disk_usage = "45 %"
        st.markdown(f"""<p class="header_text">Disk 사용률</p>
                    <p class="number_down">
                    {Disk_usage}
                    <span class="symbol_down"> ▼ </span>
                    </p>
                    """, unsafe_allow_html = True)

with col_4:
    with st.container(border=True):
        Load_average = "3.12"
        st.markdown(f"""<p class="header_text">시스템 부하</p>
                    <p class="number_up">
                    {Load_average}
                    <span class="symbol_up"> ▲ </span>
                    </p>
                    """, unsafe_allow_html = True)

with col_5:
    with st.container(border=True):
        GPU_usage = "31 %"
        st.markdown(f"""<p class="header_text">GPU 사용률</p>
                    <p class="number_down">
                    {GPU_usage}
                    <span class="symbol_down"> ▼ </span>
                    </p>
                    """, unsafe_allow_html = True)

#chart 1
st.markdown("")
col_1, col_2, col_3 = st.columns([1,1,1])
with col_1:
    with st.container(border=True):
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        st.line_chart(chart_data, height=300)
with col_2:
    with st.container(border=True):
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        st.line_chart(chart_data, height=300)
with col_3:
    with st.container(border=True):
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        st.line_chart(chart_data, height=300)



