import plotly.express as px
from modules.gjf import make_data_summary
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.chart_annotations import get_annotations_chart
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from streamlit_extras.metric_cards import style_metric_cards
from io import BytesIO
from plotly.subplots import make_subplots
from dateutil.relativedelta import relativedelta
import pandas as pd



def get_previous_year_date(date_str):
    date = datetime.strptime(date_str, '%Y%m')
    previous_year_date = date.replace(year=date.year - 1)
    return previous_year_date.strftime('%Y%m')

#Line Chart 시 6개월 전 부터 현재까지의 데이터 표출
def get_six_months_ago(date_str):
    # 날짜 문자열을 datetime 객체로 변환
    date = datetime.strptime(date_str, '%Y%m')
    
    # 6개월 전의 날짜 계산
    six_months_ago = date - relativedelta(months=5)
    
    # 결과를 'YYYYMM' 형식의 문자열로 변환
    return int(six_months_ago.strftime('%Y%m'))

#0천명 처리
def round_check(num):
    tmp = round(num/1000)%10
    return tmp

#make_data_summary에서 만든 데이터 import
df_total = make_data_summary.df_total
df_pop_comp = make_data_summary.df_pop_comp
df_pop_age = make_data_summary.df_pop_age
df_employee_ratio = make_data_summary.df_employee_ratio

# 1. 경기 인구
def population_graph(date):
    #값
    value = int(df_total.loc[df_total['PRD_DE']==date,'총인구수'].values[0])
    if round_check(value)!=0:
        value = str(round(value/1000)//10) + "만 " + str(round_check(value)) + '천명'
    else:
        value = str(round(value/1000)//10) + "만 명"
    #증감
    delta = int(df_total.loc[df_total['PRD_DE']==date,'총인구수']) - int(df_total.loc[df_total['PRD_DE']==get_previous_year_date(date),'총인구수'])
    #시각화
    st.metric(label='경기 인구', value=value, delta=f"({delta:,})")
    style_metric_cards()
    
# 2. 경기 혼인 수 
def marry_graph(date):
    if df_total.loc[(df_total['PRD_DE']==date),'혼인건수(건)'].isna().any():
         st.metric(label='경기 혼인 수', value='---값 없음---')
    else:
        #값
        value = f"{int(df_total.loc[df_total['PRD_DE']==date,'혼인건수(건)'].values[0]):,}건"
        #) + "건")
        #증감
        delta = int(df_total.loc[df_total['PRD_DE']==date,'혼인건수(건)']) - int(df_total.loc[df_total['PRD_DE']==get_previous_year_date(date),'혼인건수(건)'])
        #시각화
        st.metric(label='경기 혼인 수', value=value, delta=f"({delta:,})")
    
# 3. 경기 출생아 수 
def baby_graph(date):
    if df_total.loc[(df_total['PRD_DE']==date),'출생아수(명)'].isna().any():
         st.metric(label='경기 출생아 수', value='---값 없음---')
    else:
        #값
        #value = str(int(df_total.loc[df_total['PRD_DE']==date,'출생아수(명)'])) + "명"
        value = f"{int(df_total.loc[df_total['PRD_DE']==date,'출생아수(명)'].values[0]):,}명"
        #) + "건")
        #증감
        delta = int(df_total.loc[df_total['PRD_DE']==date,'출생아수(명)']) - int(df_total.loc[df_total['PRD_DE']==get_previous_year_date(date),'혼인건수(건)'])
        #시각화
        st.metric(label='경기 출생아 수', value=value, delta=f"({delta:,})")



# 4. 전국, 서울, 경기 인구 수 _ old_ver.
# def population_comp_graph_G_O(date):
#     trend_data = df_pop_comp.loc[(get_six_months_ago(date)<=df_pop_comp['PRD_DE'].astype(int)) & (df_pop_comp['PRD_DE'].astype(int)<= int(date))]
#     trend_data = trend_data.loc[trend_data['C1_NM']=='경기도']
#     trend_data['DT'] = trend_data['DT'].astype(int)
#     trend_data['Date'] = pd.to_datetime(trend_data['PRD_DE'], format='%Y%m')
#     trend_data['날짜'] = trend_data['Date'].dt.strftime('%Y-%m')
#     trend_data.rename(columns={'DT':'총 인구(백만 명)','C1_NM':'행정구역'},inplace=True)
#     trend_data['총 인구(백만 명)'] = round(trend_data['총 인구(백만 명)']/10000,2)
#     fig = px.line(trend_data, x='날짜', y='총 인구(백만 명)', markers = True, text='총 인구(백만 명)')
#     fig.update_xaxes(
#         tickfont={"size":13, "family": "Nanum Gothic", "color": "grey"},
#         tickformat='%Y-%m',  # 원하는 형식으로 포맷
#         tickmode='array',  # x축의 모든 값 표시
#         tickvals=trend_data['날짜'].unique(),  # x축에 표시할 값 설정
#         showline=True, linewidth=1, linecolor='black', mirror=True, #축 선 설정
#     )
#     fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False,side='left', #축 선 설정
#                      showgrid=True, gridwidth=2, gridcolor='rgba(192, 192, 192, 0.3)',
#                      tickfont={"size":13, "family": "Nanum Gothic", "color": "grey"})
#     #fig.update_yaxes(nticks=6) 날짜마다 다 바뀜..
#     fig.update_layout(
#         width=600,  # 너비를 1000픽셀로 설정
#         height=330, # 높이를 280픽셀로 설정
#         margin=dict(l=0, r=0, t=0, b=0),  # 여백을 조정하여 그래프가 꽉 차게 만듦
        
#         title_text="경기도",
#         title_x = 0.5,
#         title_y = 0.9,
#         title_xanchor = "right",
#         title_yanchor = "top",
#         #title_bgcolor= 'red'
#         #title_font_color = "색 지정",
#         #title_font_family = "폰트 지정",
#     )
#     st.plotly_chart(fig, theme="streamlit",use_container_width=True, config={'displayModeBar': False})
    
# 4. 전국, 서울, 경기 인구 수 _ new_ver.
def population_comp_graph_G(date):
    trend_data = df_pop_comp.loc[(get_six_months_ago(date)<=df_pop_comp['PRD_DE'].astype(int)) & (df_pop_comp['PRD_DE'].astype(int)<= int(date))]
    trend_data = trend_data.loc[trend_data['C1_NM']=='경기도']
    trend_data['DT'] = trend_data['DT'].astype(int)
    trend_data['Date'] = pd.to_datetime(trend_data['PRD_DE'], format='%Y%m')
    trend_data['날짜'] = trend_data['Date'].dt.strftime('%Y-%m')
    trend_data.rename(columns={'DT':'총 인구(만 명)','C1_NM':'행정구역'},inplace=True)
    trend_data['총 인구(만 명)'] = round(trend_data['총 인구(만 명)']/10000,2)
    fig = go.Figure()

    # y축 범위 설정
    y_min, y_max = trend_data['총 인구(만 명)'].min()-0.5, trend_data['총 인구(만 명)'].max()+0.5

    # 기본 데이터 트레이스
    fig.add_trace(go.Scatter(
        x=trend_data['날짜'],
        y=trend_data['총 인구(만 명)'],
        mode='lines+markers+text',
        name='경기도',
        line=dict(color='rgb(0, 100, 200)', width=2, shape='spline'),
        marker=dict(size=10, color='rgb(0, 100, 200)', line=dict(width=2, color='White')),
        text=trend_data['총 인구(만 명)'],
        textposition='top center',
        showlegend=False # legend 숨김
    ))

    #그라데이션 효과를 위한 여러 레이어 추가
    num_layers = 50
    for i in range(num_layers):
        opacity = 0.5 * (1 - i / num_layers)
        color = f'rgba(0, 100, 200, {opacity})'
        y_values = [y_min + (val - y_min) * (num_layers - i) / num_layers for val in trend_data['총 인구(만 명)']]
        fig.add_trace(go.Scatter(
            x=trend_data['날짜'],
            y=y_values,
            mode='none',
            fill='tonexty',
            fillcolor=color,
            showlegend=False
        ))

    # 레이아웃 설정
    fig.update_xaxes(
        #title_text="연월", #x축 제목
        title= dict(
            text="연월",
            standoff=20, #제목과 축 사이 간격
        ),
        tickfont={"size":13, "family": "Nanum Gothic", "color": "grey"},
        tickformat='%Y-%m',
        tickmode='array',
        tickvals=trend_data['날짜'].unique(),
        showline=True, linewidth=1, linecolor='black', mirror=False,side='left'
    )

    fig.update_yaxes(
        title_standoff=20,  # 제목과 축 사이의 간격
        automargin=True,
        range=[y_min, y_max+0.5],
        showgrid=True, gridwidth=2, gridcolor='rgba(192, 192, 192, 0.3)',
        tickfont={"size":13, "family": "Nanum Gothic", "color": "grey"},
    )

    fig.update_layout(
        width=600,
        height=420,
        margin=dict(l=50, r=20, t=40, b=0),
        showlegend=False)
    fig.add_annotation(
    text="경기도 인구(만 명)",
    x=0.5,
    y=1.05,
    xref="paper",
    yref="paper",
    showarrow=False,
    font=dict(
        family="Nanum Gothic",
        size=14,
        color="black",
        weight="normal"
    ),
    xanchor="center",
    yanchor="top"
    )
    fig.update_annotations(font_weight="normal")
    # 그래프 표시
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, config={'displayModeBar': False})











# def population_comp_graph_K(date):
#     trend_data = df_pop_comp.loc[(get_six_months_ago(date)<=df_pop_comp['PRD_DE'].astype(int)) & (df_pop_comp['PRD_DE'].astype(int)<= int(date))]
#     #trend_data = df_pop_comp.loc[df_pop_comp['PRD_DE'].astype(int) >= 202401]
#     trend_data = trend_data.loc[trend_data['C1_NM']=='전국']
#     trend_data['DT'] = trend_data['DT'].astype(int)
#     trend_data['Date'] = pd.to_datetime(trend_data['PRD_DE'], format='%Y%m')
#     trend_data['날짜'] = trend_data['Date'].dt.strftime('%Y-%m')
#     trend_data.rename(columns={'DT':'총 인구(백만 명)','C1_NM':'행정구역'},inplace=True)
#     fig = px.line(trend_data, x='날짜', y='총 인구(백만 명)', markers = True)
#     fig.update_xaxes(
#         tickfont={"size":12, "family": "Nanum Gothic", "color": "grey"},
#         tickformat='%Y-%m',  # 원하는 형식으로 포맷
#         tickmode='array',  # x축의 모든 값 표시
#         tickvals=trend_data['날짜'].unique(),  # x축에 표시할 값 설정
#         showline=True, linewidth=1, linecolor='black', mirror=True, #축 선 설정
#     )
#     fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False, side='left', #축 선 설정
#                      showgrid=True, gridwidth=2, gridcolor='rgba(192, 192, 192, 0.3)',
#                      tickfont={"size":12, "family": "Nanum Gothic", "color": "grey"},) # 그리드 라인 설정
#     #fig.update_yaxes(nticks=6) 날짜마다 다 바뀜..
#     fig.update_traces(line=dict(color='#FF6F61'))
#     fig.update_layout(
#         width=500,  # 너비를 1000픽셀로 설정
#         height=150, # 높이를 280픽셀로 설정
#         margin=dict(l=0, r=0, t=0, b=0),  # 여백을 조정하여 그래프가 꽉 차게 만듦
#     )
#     st.plotly_chart(fig, theme="streamlit",use_container_width=True, config={'displayModeBar': False})



# def population_comp_graph_S(date):
#     trend_data = df_pop_comp.loc[(get_six_months_ago(date)<=df_pop_comp['PRD_DE'].astype(int)) & (df_pop_comp['PRD_DE'].astype(int)<= int(date))]
#     trend_data = trend_data.loc[trend_data['C1_NM']=='서울특별시']
#     trend_data['DT'] = trend_data['DT'].astype(int)
#     trend_data['Date'] = pd.to_datetime(trend_data['PRD_DE'], format='%Y%m')
#     trend_data['날짜'] = trend_data['Date'].dt.strftime('%Y-%m')
#     trend_data.rename(columns={'DT':'총 인구(백만 명)','C1_NM':'행정구역'},inplace=True)
#     fig = px.line(trend_data, x='날짜', y='총 인구(백만 명)', markers = True)
#     fig.update_xaxes(
#         tickfont={"size":12, "family": "Nanum Gothic", "color": "grey"},
#         tickcolor='black',
#         tickformat='%Y-%m',  # 원하는 형식으로 포맷
#         tickmode='array',  # x축의 모든 값 표시
#         tickvals=trend_data['날짜'].unique(),  # x축에 표시할 값 설정
#         showline=True, linewidth=1, linecolor='black', mirror=True, #축 선 설정
#     )
#     fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False, side='left', #축 선 설정
#                      showgrid=True, gridwidth=2, gridcolor='rgba(192, 192, 192, 0.3)',
#                      tickfont={"size":12, "family": "Nanum Gothic", "color": "grey"}) # 그리드 라인 설정
#     fig.update_traces(line=dict(color='#FF6F61'))
#     fig.update_layout(
#         width=500,  # 너비를 1000픽셀로 설정
#         height=150, # 높이를 280픽셀로 설정
#         margin=dict(l=0, r=0, t=0, b=0),  # 여백을 조정하여 그래프가 꽉 차게 만듦
#     )
#     st.plotly_chart(fig, theme="streamlit",use_container_width=True, config={'displayModeBar': False})
    
    


####################### 전국, 서울 그래프를 동시에 그리는 방법 그라데이션 추가 ver.
def population_comp_graph_K_S(date):
    trend_data = df_pop_comp.loc[(get_six_months_ago(date)<=df_pop_comp['PRD_DE'].astype(int)) & (df_pop_comp['PRD_DE'].astype(int)<= int(date))]
    trend_data = trend_data.loc[(trend_data['C1_NM']=='서울특별시') | (trend_data['C1_NM']=='전국')]
    trend_data['DT'] = trend_data['DT'].astype(int)
    trend_data['Date'] = pd.to_datetime(trend_data['PRD_DE'], format='%Y%m')
    trend_data['날짜'] = trend_data['Date'].dt.strftime('%Y-%m')
    trend_data.rename(columns={'DT':'총 인구(만 명)','C1_NM':'행정구역'},inplace=True)
    trend_data['총 인구(만 명)'] = round(trend_data['총 인구(만 명)']/10000,2)
    
    # 전국과 서울특별시 데이터 분리
    k_data = trend_data[trend_data['행정구역']=='전국']
    s_data = trend_data[trend_data['행정구역']=='서울특별시']
    
    # y축 범위 설정
    y_min_k, y_max_k = k_data['총 인구(만 명)'].min()-0.5, k_data['총 인구(만 명)'].max()+0.5
    y_min_s, y_max_s = s_data['총 인구(만 명)'].min()-0.5, s_data['총 인구(만 명)'].max()+0.5
    
    
    #2행에 같이 그리는 subplot 준비
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=("전국 인구(만 명)", "서울 인구(만 명)"))
    
    fig.update_annotations(font_size=14, font_family="Nanum Gothic", font_weight=900, font_color='black')
    # 전국 데이터 트레이스(1행)
    fig.add_trace(
        go.Scatter(           
            x=k_data['날짜'],
            y=k_data['총 인구(만 명)'],
            mode='lines+markers+text',
            name='전국',
            line=dict(color='rgb(0,176,0)', width=2, shape='spline'),
            marker=dict(size=10, color='rgb(0,176,0)', line=dict(width=2, color='White')),
            text=k_data['총 인구(만 명)'],
            textposition='top center',
            showlegend=False # legend 숨김
            ),
        row=1, col=1)
    
    
    # 서울특별시 데이터 트레이스(2행)
    fig.add_trace(
        go.Scatter(           
            x=s_data['날짜'],
            y=s_data['총 인구(만 명)'],
            mode='lines+markers+text',
            name='서울특별시',
            line=dict(color='rgb(255,0,0)', width=2, shape='spline'),
            marker=dict(size=10, color='rgb(255,0,0)', line=dict(width=2, color='White')),
            text=s_data['총 인구(만 명)'],
            textposition='top center',
            showlegend=False # legend 숨김
            ),
        row=2, col=1)
    
    #그라데이션 효과를 위한 여러 레이어 추가_전국
    num_layers_k = 50
    for i in range(num_layers_k):
        opacity = 0.5 * (1 - i / num_layers_k)
        color = f'rgba(8, 171, 58, {opacity})'
        y_values = [y_min_k + (val - y_min_k) * (num_layers_k - i) / num_layers_k for val in k_data['총 인구(만 명)']]
        fig.add_trace(go.Scatter(
            x=k_data['날짜'],
            y=y_values,
            mode='none',
            fill='tonexty',
            fillcolor=color,
            showlegend=False
        ), row=1, col=1)
    
    #그라데이션 효과를 위한 여러 레이어 추가_서울특별시
    num_layers_s = 50
    for i in range(num_layers_s):
        opacity = 0.5 * (1 - i / num_layers_s)
        color = f'rgba(255, 59, 59, {opacity})'
        y_values = [y_min_s + (val - y_min_s) * (num_layers_s - i) / num_layers_s for val in s_data['총 인구(만 명)']]
        fig.add_trace(go.Scatter(
            x=s_data['날짜'],
            y=y_values,
            mode='none',
            fill='tonexty',
            fillcolor=color,
            showlegend=False
        ), row=2, col=1)
    
    
    # 레이아웃 설정
    fig.update_layout(
        height=420,  # 전체 높이 증가
        width=10,
        margin=dict(l=50, r=20, t=40, b=0),
        #title_text="전국 및 서울특별시 인구 추이",
        showlegend=False
    )
    
    
    # x축 설정 (공유)
    fig.update_xaxes(
        title= dict(text="     연월", standoff=20), #제목과 축 사이 간격
        tickfont={"size":13, "family": "Nanum Gothic", "color": "grey"},
        tickformat='%Y-%m',
        tickmode='array',
        tickvals=trend_data['날짜'].unique(),
        showline=True, linewidth=1, linecolor='black', mirror=False,
        row=2, col=1
    )
    
    # # 위쪽 그래프의 x축 레이블 숨기기
    # fig.update_xaxes(
    #     showticklabels=False,
    #     row=1, col=1
    # )

    
    # y축 설정
    fig.update_yaxes(
        range=[y_min_k, y_max_k+0.5],
        row=1, col=1)
    fig.update_yaxes(
        range=[y_min_s, y_max_s+0.5],
        row=2, col=1)
    

    st.plotly_chart(fig, theme="streamlit", use_container_width=True, config={'displayModeBar': False})

    





    
    
# 5. 경기 성별 인구
def mw_pop_graph(date):
    data_nm_pop = df_total.loc[df_total['PRD_DE']==date,['남자인구수','여자인구수']]
    data_nm_pop['남자인구수'] = round(int(data_nm_pop['남자인구수'])/10000,1)
    data_nm_pop['여자인구수'] = round(int(data_nm_pop['여자인구수'])/10000,1)
    data_nm_pop = data_nm_pop.melt()
    #color_map = {'남자인구수':'blue', '여자인구수':'red'}
    fig = px.pie(data_nm_pop, values = 'value', names='variable',width=250, height=180, hole=0.4,color_discrete_sequence=['#1081c4','#cc585f'])
    fig.update_traces(textposition='inside', textfont_size=18, textfont_color="white", marker_line_color="grey", marker_line_width=1, rotation=270)
    fig.update_layout(showlegend=True,
    margin=dict(t=15,b=5,l=0,r=0),
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", config={'displayModeBar': False})



# 6. 경기 연령별 인구
def age_pop_graph(date):
    bar_data = df_pop_age.loc[df_pop_age['PRD_DE']==date]
    bar_data.rename(columns={'AGE_GRP':'연령대','DT':'인구 수(만 명)'},inplace=True)
    bar_data['인구 수(만 명)'] = round(bar_data['인구 수(만 명)']/10000,2)
    fig = px.bar(bar_data, x='연령대',y='인구 수(만 명)',color='연령대', color_discrete_sequence=px.colors.sequential.Blues)
    fig.update_layout(width=50, height=165,showlegend=False, margin=dict(t=15,b=5,l=50,r=0))
    st.empty().markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig, theme="streamlit",use_container_width=True, config={'displayModeBar': False})


# 7. 경기 경제활동인구
def employee_graph(date):
    if df_total.loc[(df_total['PRD_DE']==date),'경제활동인구'].isna().any():
        st.metric(label='경기 경제활동인구', value='---값 없음---')
    else:
        #값
        #value = str(int(df_total.loc[df_total['PRD_DE']==date,'경제활동인구'])//10000) +"만 " + str(int(((int(df_total.loc[df_total['PRD_DE']==date,'경제활동인구'])%10000)/1000)+0.5)) +"천명"
        #value = f"{round((int(df_total.loc[df_total['PRD_DE']==date,'경제활동인구'].values[0])/10000)):,}만 " + str(int(((int(df_total.loc[df_total['PRD_DE']==date,'경제활동인구'])%10000)/1000))) +"천명"
        #값
        value = int(df_total.loc[df_total['PRD_DE']==date,'경제활동인구'].values[0])
        if round_check(value)!=0:
            value = str(round(value/1000)//10) + "만 " + str(round_check(value)) + '천명'
        else:
            value = str(round(value/1000)//10) + "만 명"
        #증감
        delta = int(df_total.loc[df_total['PRD_DE']==date,'경제활동인구']) - int(df_total.loc[df_total['PRD_DE']==get_previous_year_date(date),'경제활동인구'])
        #시각화
        st.metric(label='경기 경제활동인구', value=value, delta=f"({delta:,})")

# 8. 경기 실업자 수
def unemployee_graph(date):
    if df_total.loc[(df_total['PRD_DE']==date),'실업자'].isna().any():
        st.metric(label='경기 실업자 수', value='---값 없음---')
    else:
        #값
        #value = str(int(df_total.loc[df_total['PRD_DE']==date,'실업자'])//10000) +"만 " + str(int(((int(df_total.loc[df_total['PRD_DE']==date,'실업자'])%10000)/1000)+0.5)) +"천명"
        #value = f"{round((int(df_total.loc[df_total['PRD_DE']==date,'실업자'].values[0])/10000)):,}만 " + str(int(((int(df_total.loc[df_total['PRD_DE']==date,'실업자'])%10000)/1000))) +"천명"
        value = int(df_total.loc[df_total['PRD_DE']==date,'실업자'].values[0])
        if round_check(value)!=0:
            value = str(round(value/1000)//10) + "만 " + str(round_check(value)) + '천명'
        else:
            value = str(round(value/1000)//10) + "만 명"
        #증감
        delta = int(df_total.loc[df_total['PRD_DE']==date,'실업자']) - int(df_total.loc[df_total['PRD_DE']==get_previous_year_date(date),'실업자'])
        #시각화
        st.metric(label='경기 실업자 수', value=value, delta=f"({delta:,})")

# 9. 경기 사업체 수
def company_graph(date):
    if df_total.loc[(df_total['PRD_DE']==date),'사업장수(전체)'].isna().any():
        st.metric(label='경기 사업체 수', value='---값 없음---')
    else:
        #값
        #value = str(int(df_total.loc[df_total['PRD_DE']==date,'사업장수(전체)'])//10000) +"만 " + str(int(((int(df_total.loc[df_total['PRD_DE']==date,'사업장수(전체)'])%10000)/1000)+0.5)) +"천명"
        #value = f"{round((int(df_total.loc[df_total['PRD_DE']==date,'사업장수(전체)'].values[0])/10000)):,}만 "  + str(int(((int(df_total.loc[df_total['PRD_DE']==date,'사업장수(전체)'])%10000)/1000))) +"천개"
        value = int(df_total.loc[df_total['PRD_DE']==date,'사업장수(전체)'].values[0])
        if round_check(value)!=0:
            value = str(round(value/1000)//10) + "만 " + str(round_check(value)) + '천개'
        else:
            value = str(round(value/1000)//10) + "만 개"        
        #증감
        delta = int(df_total.loc[df_total['PRD_DE']==date,'사업장수(전체)']) - int(df_total.loc[df_total['PRD_DE']==get_previous_year_date(date),'사업장수(전체)'])
        #시각화
        st.metric(label='경기 사업체 수', value=value, delta=f"({delta:,})")
    
    

# 10. 경기, 서울, 전국 고용률 추이 비교
def employee_ratio_graph(date):
    trend_data = df_employee_ratio.loc[(get_six_months_ago(date)<=df_employee_ratio['PRD_DE'].astype(int)) & (df_employee_ratio['PRD_DE'].astype(int)<= int(date))]
    # if df_employee_ratio.loc[(df_employee_ratio['PRD_DE']==date),'DT'].isna().any():
    #     st.metric(label='', value='---값 없음---')
    # else:
    trend_data['DT'] = trend_data['DT'].astype(float)
    trend_data['Date'] = pd.to_datetime(trend_data['PRD_DE'], format='%Y%m')
    trend_data['연월'] = trend_data['Date'].dt.strftime('%Y-%m')
    trend_data.rename(columns={'DT':'고용률(%)','C1_NM':'행정구역'},inplace=True)
    fig = px.line(trend_data, x='연월', y='고용률(%)',color='행정구역', markers = True, color_discrete_sequence=['rgb(0,176,0)','rgb(255,0,0)','rgb(0,100,200)'], line_shape='spline')
    fig.update_xaxes(
         tickfont={"size":13, "family": "Nanum Gothic", "color": "grey"},
        tickformat='%Y-%m',  # 원하는 형식으로 포맷
        tickmode='array',  # x축의 모든 값 표시
        tickvals=trend_data['연월'].unique(), # x축에 표시할 값 설정
        showline=True, linewidth=1, linecolor='black',mirror=True #축 선 설정
    )
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=False,side='left', #축 선 설정
                     showgrid=True, gridwidth=2, gridcolor='rgba(192, 192, 192, 0.3)',
                     tickfont={"size":13, "family": "Nanum Gothic", "color": "grey"})
    fig.update_layout(
    width=150,  # 
    height=270, # 
    margin=dict(l=0, r=0, t=0, b=0),  # 여백을 조정하여 그래프가 꽉 차게 만듦
    )
    st.empty().markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig, theme="streamlit",use_container_width=True, config={'displayModeBar': False})
    
# 11. 경기 구인구직 비교 인구
def recruit_graph(date):
    if df_total.loc[(df_total['PRD_DE']==date),'구인인원(월)'].isna().any() | df_total.loc[(df_total['PRD_DE']==date),'구직건수(월)'].isna().any() :
        st.metric(label='', value='---값 없음---')
    else:
        data_recruit = df_total.loc[df_total['PRD_DE']==date,['구인인원(월)','구직건수(월)']]
        data_recruit.rename(columns={'구인인원(월)': '구인인원(명)', '구직건수(월)': '구직건수(건)'},inplace=True)
        data_recruit = data_recruit.melt()
        fig = px.pie(data_recruit, values = 'value', names='variable',width=250, height=250, hole=.4, color_discrete_sequence=['#08519C','#6BAED6'])
        fig.update_traces(textposition='inside',textfont_size=15,marker_line_color="grey",marker_line_width=1, textinfo='value')
        fig.update_layout(legend=dict(
        orientation='h',
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5),
        margin=dict(t=20,b=0,l=0,r=0)
        )
        st.empty().markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", config={'displayModeBar': False})
