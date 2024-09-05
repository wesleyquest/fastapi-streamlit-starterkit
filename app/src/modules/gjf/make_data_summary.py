import json
from urllib.request import urlopen
from datetime import datetime
from dateutil.relativedelta import relativedelta
import datetime as dt
from functools import reduce
import pandas as pd
import os
import openpyxl

# 1.1 경기 인구, 성별 인구 통계
api_url_pop = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI=\
&itmId=T20+T21+T22+&objL1=41+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M\
&startPrdDe=202301&endPrdDe=202407\
&orgId=101&tblId=DT_1B040A3'

with urlopen(api_url_pop) as url:
    json_file = url.read()
    py_json = json.loads(json_file.decode('utf-8'))
    df_pop = pd.DataFrame(py_json)
    
#필요 컬럼 필터링
df_pop = df_pop[['PRD_DE','ITM_NM','DT','UNIT_NM']]
df_pop_pivot = df_pop.pivot_table(index='PRD_DE', columns='ITM_NM',values='DT',aggfunc='sum').reset_index()



# 1.2 서울, 전국 총 인구 
api_url_pop_comp = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI=\
&itmId=T20+T21+T22+&objL1=00+11+41+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M\
&startPrdDe=202301&endPrdDe=202407\
&orgId=101&tblId=DT_1B040A3'


with urlopen(api_url_pop_comp) as url:
    json_file = url.read()
    py_json = json.loads(json_file.decode('utf-8'))
    df_pop_comp = pd.DataFrame(py_json)
    
#필요 컬럼 필터링
df_pop_comp = df_pop_comp[df_pop_comp['ITM_NM']=='총인구수']
df_pop_comp = df_pop_comp[['PRD_DE','DT','C1_NM']]
df_pop_comp



# 2. 경기 연령별 인구 통계
# 2.1 전처리 함수 정의
def age_group(age_str):
    age = int(age_str)
    if age <= 10:
        return '09세 이하'
    elif 10 < age <= 20:
        return '10대'
    elif 20 < age <= 30:
        return '20대'
    elif 30 < age <= 40:
        return '30대'
    elif 40 < age <= 50:
        return '40대'
    elif 50 < age <= 60:
        return '50대'
    elif 60 < age <= 70:
        return '60대'
    elif 70 < age <= 80:
        return '70대'
    else :
        return '80대 이상'
    
# 2.2 통계
api_url_pop_age = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&\
apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI=&itmId=T2+&objL1=41+&objL2=5+10+15+20+25+30+35+40+45+50+55+60+65+70+75+80+85+90+95+100+105+&objL3=&\
objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&\
startPrdDe=202301&endPrdDe=202407&orgId=101&tblId=DT_1B04005N'

with urlopen(api_url_pop_age) as url:
    json_file = url.read()
    py_json = json.loads(json_file.decode('utf-8'))
    df_pop_age = pd.DataFrame(py_json)

df_pop_age['AGE_GRP'] = df_pop_age['C2'].apply(age_group)
df_pop_age['DT'] = df_pop_age['DT'].astype(int)
df_pop_age = df_pop_age[['PRD_DE','AGE_GRP','DT']]
df_pop_age = df_pop_age.groupby(['PRD_DE','AGE_GRP']).sum()['DT']
df_pop_age = df_pop_age.reset_index()
df_pop_age = df_pop_age.loc[df_pop_age['PRD_DE'].astype(int) >= 202401]


# 3. 경기 혼인건수, 출생아 수 통계
api_url_mary_baby = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList\
&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI=\
&itmId=T1+&objL1=31+&objL2=10+20+&objL3=&objL4=&objL5=&objL6=&objL7=\
&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=202301&endPrdDe=202405&orgId=101&tblId=DT_1B8000G'
with urlopen(api_url_mary_baby) as url:
    json_file = url.read()
    py_json = json.loads(json_file.decode('utf-8'))
    df_mary_baby = pd.DataFrame(py_json)
df_mary_baby_pivot = df_mary_baby.pivot_table(index='PRD_DE', columns='C2_NM',values='DT',aggfunc='max').reset_index()
df_mary_baby_pivot.columns.name = None # 매우 중요

# 4. 경기 경제활동인구, 취업, 실업자 수 통계
api_url_employee ='https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI=\
&itmId=T20+T30+T40+&objL1=31+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&\
startPrdDe=202301&endPrdDe=202406&orgId=101&tblId=DT_1DA7004S'

with urlopen(api_url_employee) as url:
    json_file = url.read()
    py_json = json.loads(json_file.decode('utf-8'))
    df_employee = pd.DataFrame(py_json)
df_employee_pivot = df_employee.pivot_table(index='PRD_DE', columns='ITM_NM',values='DT',aggfunc='max').reset_index()
df_employee_pivot['경제활동인구'] = df_employee_pivot['경제활동인구'].astype(float) * 1000
df_employee_pivot['취업자'] = df_employee_pivot['취업자'].astype(float) * 1000
df_employee_pivot['실업자'] = df_employee_pivot['실업자'].astype(float) * 1000

# 4.2 실업률 통계
api_url_ratio_employee = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI=&itmId=T90+&objL1=00+11+31+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=202301&endPrdDe=202406&orgId=101&tblId=DT_1DA7004S'
with urlopen(api_url_ratio_employee) as url:
    json_file = url.read()
    py_json = json.loads(json_file.decode('utf-8'))
    df_employee_ratio = pd.DataFrame(py_json)
df_employee_ratio = df_employee_ratio[['PRD_DE','C1_NM','DT']]
df_employee_ratio['C1_NM'] = df_employee_ratio['C1_NM'].replace('계','전국')
df_employee_ratio


# 5. 구인구직통계
# 5.1 전처리 함수 정의
def format_date_recruit(date_str):
    year, month = date_str.split('년 ')
    month = month.replace('월', '')
    return f"{year}{month.zfill(2)}"

# 5.2 통계
print('****************현재경로*****************')
print(os.getcwd())
df_recruit = pd.read_excel('/app/src/modules/gjf/구인구직취업현황(월).xlsx')
df_recruit = df_recruit.loc[df_recruit['출처']!='총계']
df_recruit.columns = df_recruit.iloc[12]
df_recruit = df_recruit.iloc[13:]
df_recruit['PRD_DE'] = df_recruit['마감년월'].apply(format_date_recruit)
df_recruit = df_recruit.drop(columns=['마감년월'])

# 6. 사업체통계
# 6.1 전처리 함수 정의
def format_date_company(date_str):
    year, month = date_str.split('년')
    month = month.replace('월', '')
    return f"{year}{month.zfill(2)}"

# 6.2 통계
df_company = pd.read_excel('/app/src/modules/gjf/사업장현황(전체).xlsx')
df_company = df_company.loc[df_company['출처']!='총계']
df_company.columns = df_company.iloc[12]
df_company = df_company.iloc[13:]
df_company['PRD_DE'] = df_company['마감년월'].apply(format_date_company)
df_company = df_company.drop(columns=['마감년월'])

# 7. Merge

df_list = [df_pop_pivot,df_mary_baby_pivot,df_employee_pivot,df_recruit,df_company]
df_total = reduce(lambda x,y : pd.merge(x,y, on='PRD_DE',how='outer'),df_list)
pd.set_option('display.max_columns', None)
df_total
