############################################################################
#경기도 데이터 분석 (경기일자리재단)
############################################################################


import streamlit as st

from modules.settings.page import set_page_config, make_sidebar
from modules.settings.style import style_global
from modules.auth.api_auth import validate_token, get_user_info

from modules.gjf import make_graph_new as make_graph
import pandas as pd
import plotly.express as px
import datetime as dt
from dateutil.relativedelta import relativedelta
# from tkinter.tix import COLUMN
from pyparsing import empty
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards

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
##############################################################################
#custom style
st.markdown("")
#main

#연월 초기값 설정
if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = '2024년 05월' # 초기값 설정.



##title
col_1, col_2 = st.columns([1,1])
with col_1:
    #st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 경기도 데이터 분석 </div>""", unsafe_allow_html=True)
    #st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 경기도 데이터 분석({selected_date_O}) </div>""", unsafe_allow_html=True)    
    #st.markdown(f"""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 경기도 데이터 분석({selected_date_O}) </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 경기도 데이터 분석({st.session_state["selected_date"]}🚀) </div>""", unsafe_allow_html=True)
with col_2:
    col_2_1, col_2_2, col_2_3 = st.columns([8,1,1])
    with col_2_1:
        date_list = [f'2024년 {str(i).zfill(2)}월' for i in range(1,8)]
        default_option = st.session_state['selected_date']
        # st.markdown('##### 연월을 선택하세요')
        option = st.selectbox('',date_list,index=date_list.index(default_option), label_visibility="collapsed")
        if option != st.session_state['selected_date']:
            st.session_state['selected_date'] = option
            #st.experimental_rerun() # 선택된 값으로 타이틀 갱신을 위한 재실행
            st.rerun() # 선택된 값으로 타이틀 갱신을 위한 재실행
    with col_2_2:
        if st.button(":material/account_circle:",key="df", use_container_width=False):
            st.switch_page("pages/my_profile.py")
    with col_2_3:     
        if st.button(":material/logout:",key="asdf", use_container_width=False):
            st.session_state = {}
            st.switch_page("main.py")
st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
st.markdown("")

#선택한 연월 데이터 형식에 맞게 처리
selected_date_code = '2024'+ st.session_state['selected_date'][6:8]

#여백줄 겸 Metric 스타일 정의
st.markdown("""
<style>

div[data-testid="stVerticalBlockBorderWrapper"] .st-emotion-cache-1hmkk4d {
    padding-bottom: 0px !important; /* Remove all padding */
}

div[data-testid="stVerticalBlockBorderWrapper"] .st-emotion-cache-16f0cpy {
    padding-bottom: 0px !important; /* Remove all padding */
}

/* Adjust the font size of the label */
div[data-testid="stMetric"] p:first-of-type {
    font-size: 17px !important; /* Use !important to ensure it overrides other styles */
    padding: 0px !important; /* Remove all padding */
}

/* Adjust the font size of the value */
div[data-testid="stMetricValue"] {
    font-size: 24px; /* Adjust this value as needed */
    text-align: center; /* Center-align the value */
    padding: 0px !important; /* Remove all padding */
}

/* Adjust the font size of the delta */
div[data-testid="stMetric"] div[data-testid="stMetricDelta"]{
    font-size: 20px; /* Adjust this value as needed */
    font-weight: bold; /* Make the delta text bold */
    text-align: center; /* Center-align the value */
    padding: 0px !important; /* Remove all padding */
}

[data-testid="stMetricDelta"] > svg {
position: absolute;
right: 10%;
-webkit-transform: translateX(-50%);
-ms-transform: translateX(-50%);
transform: translateX(-50%);
}

div[data-testid="stMetric"] {
padding: 5px !important; /* Remove all padding */
}
</style>
""", unsafe_allow_html=True)


#1. 인구 통계
st.subheader('1. 인구 통계👪',anchor=False)

# 1st layer - Metric
with st.container(height=130):
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        make_graph.population_graph(selected_date_code)
    with col2:
        make_graph.marry_graph(selected_date_code)
    with col3:
        make_graph.baby_graph(selected_date_code)
        
    
# 2nd layer -  new_ver._20240813
with st.container(height=480):
    st.markdown("""
                <div style="padding-left: -5px; padding-top: -5px; ">
                    <span style= "font-size: 17px;">
                        경기, 전국, 서울 인구 추세 비교
                    </span>
                </div>
                """, 
                unsafe_allow_html=True)
    # 큰 그래프와 작은 그래프들을 위한 두 개의 컬럼
    with st.container():
        col_left, col_right = st.columns([1, 1])
        # 왼쪽에 큰 그래프 배치
        with col_left:
            # st.markdown("""
            #         <div style="padding-top: 0px; padding-bottom: 10px;">
            #             <p style= "text-align: center; font-size: 15px;">
            #                  경기도
            #             </p>
            #         </div>
            #         """, unsafe_allow_html=True)
            make_graph.population_comp_graph_G(selected_date_code)

        # 오른쪽에 두 개의 작은 그래프 배치
        with col_right:
            make_graph.population_comp_graph_K_S(selected_date_code)
            # st.markdown("""
            #             <div style="text-align: center;">
            #             <p style= "text-align: center; font-size: 15px; padding-top: 5px; padding-bottom: 5px; padding-left: 5px;">
            #                  전국
            #             </p>
            #             </div>
            #             """, unsafe_allow_html=True)
            # population_comp_graph_K(selected_date_code)

            # st.markdown("""
            #             <div style="text-align: center;">
            #             <p style= "text-align: center; font-size: 15px;">
            #                  서울
            #             </p>
            #             </div>
            #             """, unsafe_allow_html=True)
            # population_comp_graph_S(selected_date_code)
            
            
            
            
# 3rd layer
with st.container():
    col_left, col_right = st.columns([0.4, 0.6])
    with col_left:
        with st.container(height=240):
            st.markdown("""
            <span style= "font-size: 17px;">
                경기 성별 인구
            </span>
            """, unsafe_allow_html=True
            )
            make_graph.mw_pop_graph(selected_date_code)
    with col_right:
        with st.container(height=240):
            st.markdown("""
            <span style= "font-size: 17px;">
                경기 연령별 인구
            </span>
            """, unsafe_allow_html=True
            )
            make_graph.age_pop_graph(selected_date_code)
            

#여백 줄 
st.write('')

#2. 일자리 통계
st.subheader('2. 일자리 통계👨‍💼👩‍💼',anchor=False)

# 4st layer - Metric
with st.container(height=130):
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        make_graph.employee_graph(selected_date_code)
    with col2:
        make_graph.unemployee_graph(selected_date_code)
    with col3:
        make_graph.company_graph(selected_date_code)
        
# 5st layer
with st.container():
    col_left, col_right = st.columns([0.7, 0.3])
    with col_left:
        with st.container(height=360):
            st.markdown("""
            <span style= "font-size: 17px;">
                고용률 경기, 전국, 서울 비교
            </span>
            """, unsafe_allow_html=True
            )
            make_graph.employee_ratio_graph(selected_date_code)
    with col_right:
        with st.container(height=360):
            st.markdown("""
            <span style= "font-size: 17px;">
                경기 구인구직 비교
            </span>
            """, unsafe_allow_html=True
            )
            make_graph.recruit_graph(selected_date_code)
