import streamlit as st
import pandas as pd
from modules.settings.style import style_global
from modules.settings.page import set_page_config, make_sidebar
from modules.auth.api_auth import validate_token, get_user_info
#custom_modules
from modules.data_extraction_htc.custom_func import read_ois_table, transform_ois_data, read_lims_table, transform_lims_data
import datetime
import time
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

##custom session state
if "analyzer_data_1_options" not in st.session_state:
    st.session_state["analyzer_data_1_options"] = {}
    st.session_state["analyzer_data_1_options"]["tag"] = ['BTI215', 'BPIC211', 'BFFC204', 'BFIC471', 'BTI210', 'BPI207', 'BTI234', 'BPIC238']
    st.session_state["analyzer_data_1_options"]["gigan_date_input"] = (datetime.date(2024, 5, 1), datetime.date(2024, 6, 30))
    st.session_state["analyzer_data_1_options"]["time_unit_radio"] = "시간 단위"
    st.session_state["analyzer_data_1_options"]["time_unit_number_slider"] = 1
if "analyzer_data_2_options" not in st.session_state:
    st.session_state["analyzer_data_2_options"] = {}
    st.session_state["analyzer_data_2_options"]["sample_point"] = 'SC201'
    st.session_state["analyzer_data_2_options"]["item_name"] = ['N-Aro8', 'Ethylbenzene', 'p&m-Xylene', 'o-Xylene']
    st.session_state["analyzer_data_2_options"]["gigan_date_input"] = (datetime.date(2024, 5, 1), datetime.date(2024, 6, 30))
    st.session_state["analyzer_data_2_options"]["time_unit_radio"] = "시간 단위"
    st.session_state["analyzer_data_2_options"]["time_unit_number_slider"] = 1



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
    st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 데이터 추출 </div>""", unsafe_allow_html=True)
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

##dialog(modal)
@st.dialog("데이터 추출 조건을 선택하세요")
def select_options_analyzer_data_1():
    with st.container(border=True):
        data_1_tag_multiselect = st.multiselect(
            "1 - 태그를 선택하세요",
            ["BTI215", "BPIC211", "BFFC204", "BFIC471", "BTI210", "BPI207", "BTI234", "BPIC238"],
            ["BTI215", "BPIC211", "BFFC204", "BFIC471", "BTI210", "BPI207", "BTI234", "BPIC238"],
        )

    with st.container(border=True):
        today = datetime.datetime.now()

        data_1_gigan_date_input = st.date_input(
            "2 - 기간을 선택하세요",
            (datetime.date(today.year, today.month, 1), datetime.date(today.year, today.month, today.day)),
            datetime.date(today.year-9, 1, 1),
            datetime.date(today.year, today.month, today.day),
            format="YYYY-MM-DD",
        )

    with st.container(border=True):
        data_1_time_unit_radio = st.radio(
            "3.1 - 단위 기준을 선택하세요",
            ["년 단위", "월 단위", "일 단위", "시간 단위", "분 단위"],
            index=3,
        )
          
        if data_1_time_unit_radio == "년 단위":
            data_1_time_unit_number_slider = st.slider("3.2 - 몇 년 단위인가요?", 1, 10, 1)
        elif data_1_time_unit_radio == "월 단위":
            data_1_time_unit_number_slider = st.slider("3.2 - 몇 개월 단위인가요? ", 1, 12, 1)
        elif data_1_time_unit_radio == "일 단위":
            data_1_time_unit_number_slider = st.slider("3.2 - 몇 일 단위인가요? ", 1, 31, 1)
        elif data_1_time_unit_radio == "시간 단위":
            data_1_time_unit_number_slider = st.slider("3.2 - 몇 시간 단위인가요? ", 1, 24, 1)
        else:
            data_1_time_unit_number_slider = st.slider("3.2 - 몇 분 단위인가요? ", 1, 60, 1)

        if data_1_time_unit_radio:
            st.info(f"**※ {str(data_1_time_unit_number_slider)} {data_1_time_unit_radio} 데이터를 선택했어요**")

    col_1, col_2 = st.columns([1,1], gap="large")
    with col_1:
        if st.button("&nbsp; 취 소 &nbsp;", use_container_width=True):
            st.rerun()
    with col_2:
        if st.button("&nbsp; 적 용 &nbsp;", type="primary", use_container_width=True):
            st.session_state["analyzer_data_1_options"] = {}
            st.session_state["analyzer_data_1_options"]["tag"] = data_1_tag_multiselect
            st.session_state["analyzer_data_1_options"]["gigan_date_input"] = data_1_gigan_date_input
            st.session_state["analyzer_data_1_options"]["time_unit_radio"] = data_1_time_unit_radio  
            st.session_state["analyzer_data_1_options"]["time_unit_number_slider"] = data_1_time_unit_number_slider
            st.rerun()

@st.dialog("데이터 추출 조건을 선택하세요")
def select_options_analyzer_data_2():
    with st.container(border=True):
        data_2_sample_point_selectbox = st.selectbox(
            "1 - 샘플포인트(SAMPLE_POINT)를 선택하세요",
            ('SC201', "추가 예정"),
            index=0,
        )
    with st.container(border=True):
        data_2_item_name_multiselect = st.multiselect(
            "2 - 아이템명(ITEM_NAME)을 선택하세요",
            ['N-Aro8', 'Ethylbenzene', 'p&m-Xylene', 'o-Xylene'],
            ['N-Aro8', 'Ethylbenzene', 'p&m-Xylene', 'o-Xylene'],
        )

    with st.container(border=True):
        today = datetime.datetime.now()

        data_2_gigan_date_input = st.date_input(
            "2 - 기간을 선택하세요",
            (datetime.date(today.year, today.month, 1), datetime.date(today.year, today.month, today.day)),
            datetime.date(today.year-9, 1, 1),
            datetime.date(today.year, today.month, today.day),
            format="YYYY-MM-DD",
        )

    with st.container(border=True):
        data_2_time_unit_radio = st.radio(
            "3.1 - 단위 기준을 선택하세요",
            ["년 단위", "월 단위", "일 단위", "시간 단위", "분 단위"],
            index=3,
        )
          
        if data_2_time_unit_radio == "년 단위":
            data_2_time_unit_number_slider = st.slider("3.2 - 몇 년 단위인가요?", 1, 10, 1)
        elif data_2_time_unit_radio == "월 단위":
            data_2_time_unit_number_slider = st.slider("3.2 - 몇 개월 단위인가요? ", 1, 12, 1)
        elif data_2_time_unit_radio == "일 단위":
            data_2_time_unit_number_slider = st.slider("3.2 - 몇 일 단위인가요? ", 1, 31, 1)
        elif data_2_time_unit_radio == "시간 단위":
            data_2_time_unit_number_slider = st.slider("3.2 - 몇 시간 단위인가요? ", 1, 24, 1)
        else:
            data_2_time_unit_number_slider = st.slider("3.2 - 몇 분 단위인가요? ", 1, 60, 1)

        if data_2_time_unit_radio:
            st.info(f"**※ {str(data_2_time_unit_number_slider)} {data_2_time_unit_radio} 데이터를 선택했어요**")

    col_1, col_2 = st.columns([1,1], gap="large")
    with col_1:
        if st.button("&nbsp; 취 소 &nbsp;", use_container_width=True):
            st.rerun()
    with col_2:
        if st.button("&nbsp; 적 용 &nbsp;", type="primary", use_container_width=True):
            st.session_state["analyzer_data_2_options"] = {}
            st.session_state["analyzer_data_2_options"]["sample_point"] = data_2_sample_point_selectbox
            st.session_state["analyzer_data_2_options"]["item_name"] = data_2_item_name_multiselect
            st.session_state["analyzer_data_2_options"]["gigan_date_input"] = data_2_gigan_date_input
            st.session_state["analyzer_data_2_options"]["time_unit_radio"] = data_2_time_unit_radio  
            st.session_state["analyzer_data_2_options"]["time_unit_number_slider"] = data_2_time_unit_number_slider
            st.rerun()

##content
main_col_1, main_col_2, main_col_3 = st.columns([2.5,5,2.5])
with main_col_2:    
    tab_1, tab_2 = st.tabs(["**Analyzer data from OIS**", "**Analyzer data from LIMS**"])
    
    with tab_1:
        with st.container(border=True):
    
            data_1_selected_tag_list = st.session_state["analyzer_data_1_options"]["tag"]
            data_1_selected_gigan_text = f"""
            {st.session_state["analyzer_data_1_options"]["gigan_date_input"][0].year}-{st.session_state["analyzer_data_1_options"]["gigan_date_input"][0].month}-{st.session_state["analyzer_data_1_options"]["gigan_date_input"][0].day}
                ~ 
            {st.session_state["analyzer_data_1_options"]["gigan_date_input"][1].year}-{st.session_state["analyzer_data_1_options"]["gigan_date_input"][1].month}-{st.session_state["analyzer_data_1_options"]["gigan_date_input"][1].day}"""
            data_1_selected_time_unit = str(st.session_state["analyzer_data_1_options"]["time_unit_number_slider"]) +" "+ st.session_state["analyzer_data_1_options"]["time_unit_radio"]
            
            st.markdown("**📢 현재 추출 조건을 확인하세요!**")
            st.markdown(f"""
                        **1 - 선택 태그** :  
                        :red-background[{data_1_selected_tag_list}]  
                        **2 - 추출 기간** :  
                        :red-background[{data_1_selected_gigan_text}]  
                        **3 - 추출 단위** :  
                        :red-background[{data_1_selected_time_unit}]
                        """)
            st.markdown("")
            col_1, col_2 = st.columns([1,1], gap="large")
    
            with col_1:
                if st.button("🕹️ 조건 수정", key="data_1_setting_button", use_container_width=True):
                    select_options_analyzer_data_1()
            with col_2:
                data_1_extract_button = st.button("🚀 추출 시작", key="data_1_start_button", type="primary", use_container_width=True)
    
    
        if data_1_extract_button:
    
            #set parameters
            data_1_start_date = st.session_state["analyzer_data_1_options"]["gigan_date_input"][0].strftime("%Y%m%d")
            data_1_end_date = st.session_state["analyzer_data_1_options"]["gigan_date_input"][1].strftime("%Y%m%d")
            data_1_target_tag = tuple(st.session_state["analyzer_data_1_options"]["tag"])
    
            if st.session_state["analyzer_data_1_options"]["time_unit_radio"] == "시간 단위":
                data_1_time_unit = str(st.session_state["analyzer_data_1_options"]["time_unit_number_slider"]) + "h"
            elif st.session_state["analyzer_data_1_options"]["time_unit_radio"] == "분 단위":
                data_1_time_unit = str(st.session_state["analyzer_data_1_options"]["time_unit_number_slider"]) + "min"
            elif st.session_state["analyzer_data_1_options"]["time_unit_radio"] == "일 단위":
                data_1_time_unit = str(st.session_state["analyzer_data_1_options"]["time_unit_number_slider"]) + "d"
            elif st.session_state["analyzer_data_1_options"]["time_unit_radio"] == "월 단위":
                data_1_time_unit = str(st.session_state["analyzer_data_1_options"]["time_unit_number_slider"]) + "MS"
            else: #연 단위
                data_1_time_unit = str(st.session_state["analyzer_data_1_options"]["time_unit_number_slider"]) + "YS"
    
    
            data_1_progress_text = "☑️ 세션 및 조건값을 불러오는 중입니다. 잠시만 기다려 주세요."
            data_1_my_bar = st.progress(10, text=data_1_progress_text)
            time.sleep(0.5)
            data_1_progress_text = "☑️ OIS 데이터를 불러오는 중입니다. 잠시만 기다려 주세요."
            data_1_my_bar.progress(35, text=data_1_progress_text)
            data_1_ois_table = read_ois_table(data_1_start_date, data_1_end_date, data_1_target_tag)
            if len(data_1_ois_table)>0:
                data_1_progress_text = "☑️ 데이터를 변환 중입니다. 잠시만 기다려 주세요."
                data_1_my_bar.progress(65, text=data_1_progress_text)
                time.sleep(0.5)
                data_1_transformed_data = transform_ois_data(data_1_ois_table, "EVENT_TIME", data_1_time_unit)
                data_1_progress_text = "☑️ 완료!"
                data_1_my_bar.progress(100, text=data_1_progress_text)
                time.sleep(0.5)
                data_1_my_bar.empty()
    
                st.info("**🆗 데이터 추출이 완료되었습니다. 샘플을 확인하고 다운로드 하세요**")
                
                with st.container(border=True):
                    st.markdown("데이터 샘플")
                    st.dataframe(data_1_transformed_data.head(100), use_container_width=True)
                    data_1_csv = data_1_transformed_data.to_csv(index=False).encode("utf-8")
                    st.markdown("데이터 다운로드")
                    st.download_button(
                        label="Download data as CSV",
                        data=data_1_csv,
                        file_name="analyzer_data_from_ois.csv",
                        mime="text/csv",
                        type="primary",
                        use_container_width=True
                    )
            else:
                data_1_my_bar.empty()
                st.info("**❌ 해당 조건에 데이터가 없습니다. 추출 조건을 수정하세요**")
    
    with tab_2:
        #st.error("준비 중입니다. 관리자에게 문의하세요")
        with st.container(border=True):
    
            data_2_selected_sample_point = st.session_state["analyzer_data_2_options"]["sample_point"]
            data_2_selected_item_name_list = st.session_state["analyzer_data_2_options"]["item_name"]
            data_2_selected_gigan_text = f"""
            {st.session_state["analyzer_data_2_options"]["gigan_date_input"][0].year}-{st.session_state["analyzer_data_2_options"]["gigan_date_input"][0].month}-{st.session_state["analyzer_data_2_options"]["gigan_date_input"][0].day}
                ~ 
            {st.session_state["analyzer_data_2_options"]["gigan_date_input"][1].year}-{st.session_state["analyzer_data_2_options"]["gigan_date_input"][1].month}-{st.session_state["analyzer_data_2_options"]["gigan_date_input"][1].day}"""
            data_2_selected_time_unit = str(st.session_state["analyzer_data_2_options"]["time_unit_number_slider"]) +" "+ st.session_state["analyzer_data_2_options"]["time_unit_radio"]
            
            st.markdown("**📢 현재 추출 조건을 확인하세요!**")
            st.markdown(f"""
                        **1 - 선택 샘플포인트** :  
                        :red-background[{data_2_selected_sample_point}]  
                        **2 - 선택 아이템명** :  
                        :red-background[{data_2_selected_item_name_list}]                      
                        **3 - 추출 기간** :  
                        :red-background[{data_2_selected_gigan_text}]  
                        **4 - 추출 단위** :  
                        :red-background[{data_2_selected_time_unit}]
                        """)
            st.markdown("")
            col_1, col_2 = st.columns([1,1], gap="large")
    
            with col_1:
                if st.button("🕹️ 조건 수정", key="data_2_setting_button", use_container_width=True):
                    select_options_analyzer_data_2()
            with col_2:
                data_2_extract_button = st.button("🚀 추출 시작", key="data_2_start_button", type="primary", use_container_width=True)
    
        if data_2_extract_button:
    
            #set parameters
            data_2_start_date = st.session_state["analyzer_data_2_options"]["gigan_date_input"][0].strftime("%Y%m%d")
            data_2_end_date = st.session_state["analyzer_data_2_options"]["gigan_date_input"][1].strftime("%Y%m%d")
            data_2_sample_point = st.session_state["analyzer_data_2_options"]["sample_point"]
            data_2_item_name = tuple(st.session_state["analyzer_data_2_options"]["item_name"])
    
            if st.session_state["analyzer_data_2_options"]["time_unit_radio"] == "시간 단위":
                data_2_time_unit = str(st.session_state["analyzer_data_2_options"]["time_unit_number_slider"]) + "h"
            elif st.session_state["analyzer_data_2_options"]["time_unit_radio"] == "분 단위":
                data_2_time_unit = str(st.session_state["analyzer_data_2_options"]["time_unit_number_slider"]) + "min"
            elif st.session_state["analyzer_data_2_options"]["time_unit_radio"] == "일 단위":
                data_2_time_unit = str(st.session_state["analyzer_data_2_options"]["time_unit_number_slider"]) + "d"
            elif st.session_state["analyzer_data_2_options"]["time_unit_radio"] == "월 단위":
                data_2_time_unit = str(st.session_state["analyzer_data_2_options"]["time_unit_number_slider"]) + "MS"
            else: #연 단위
                data_2_time_unit = str(st.session_state["analyzer_data_2_options"]["time_unit_number_slider"]) + "YS"
    
    
            data_2_progress_text = "☑️ 세션 및 조건값을 확인 중입니다. 잠시만 기다려 주세요."
            data_2_my_bar = st.progress(10, text=data_2_progress_text)
            time.sleep(0.5)
            data_2_progress_text = "☑️ LIMS 데이터를 불러오는 중입니다. 잠시만 기다려 주세요."
            data_2_my_bar.progress(35, text=data_2_progress_text)
            data_2_lims_table = read_lims_table(data_2_start_date, data_2_end_date, data_2_sample_point, data_2_item_name)
            if len(data_2_lims_table)>0:
                data_2_progress_text = "☑️ 데이터를 변환 중입니다. 잠시만 기다려 주세요."
                data_2_my_bar.progress(65, text=data_2_progress_text)
                time.sleep(0.5)
                data_2_transformed_data = transform_lims_data(data_2_lims_table, "SAMPLING_DATE", data_2_time_unit)
                
                data_2_progress_text = "☑️ 완료!"
                data_2_my_bar.progress(100, text=data_2_progress_text)
                time.sleep(0.5)
                data_2_my_bar.empty()
    
                st.info("**🆗 데이터 추출이 완료되었습니다. 샘플을 확인하고 다운로드 하세요**")
                
                with st.container(border=True):
                    st.markdown("데이터 샘플")
                    st.dataframe(data_2_transformed_data.head(100), use_container_width=True)
                    data_2_csv = data_2_transformed_data.to_csv(index=False).encode("utf-8")
                    st.markdown("데이터 다운로드")
                    st.download_button(
                        label="Download data as CSV",
                        data=data_2_csv,
                        file_name="analyzer_data_from_lims.csv",
                        mime="text/csv",
                        type="primary",
                        use_container_width=True
                    )
            else:
                data_2_my_bar.empty()
                st.info("**❌ 해당 조건에 데이터가 없습니다. 추출 조건을 수정하세요**")

