import json
from urllib.request import urlopen
from functools import reduce
import pandas as pd
import os
import psycopg2

def get_pop_pivot():
    # 1.1 경기 인구, 성별 인구 통계
    api_url_pop = "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI="\
    "&itmId=T20+T21+T22+&objL1=41+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M"\
    "&startPrdDe=202301&endPrdDe=202407"\
    "&orgId=101&tblId=DT_1B040A3"

    with urlopen(api_url_pop) as url:
        json_file = url.read()
        py_json = json.loads(json_file.decode('utf-8'))
        df_pop = pd.DataFrame(py_json)

    #필요 컬럼 필터링
    df_pop = df_pop[['PRD_DE','ITM_NM','DT','UNIT_NM']]
    df_pop_pivot = df_pop.pivot_table(index='PRD_DE', columns='ITM_NM',values='DT',aggfunc='sum').reset_index()
    return df_pop_pivot


def get_pop_comp():
    # 1.2 서울, 전국 총 인구 
    api_url_pop_comp = "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI="\
    "&itmId=T20+T21+T22+&objL1=00+11+41+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M"\
    "&startPrdDe=202301&endPrdDe=202407"\
    "&orgId=101&tblId=DT_1B040A3"


    with urlopen(api_url_pop_comp) as url:
        json_file = url.read()
        py_json = json.loads(json_file.decode('utf-8'))
        df_pop_comp = pd.DataFrame(py_json)
        
    #필요 컬럼 필터링
    df_pop_comp = df_pop_comp[df_pop_comp['ITM_NM']=='총인구수']
    df_pop_comp = df_pop_comp[['PRD_DE','DT','C1_NM']]
    return df_pop_comp



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

def get_pop_age():
    # 2.2 통계
    api_url_pop_age = "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&"\
    "apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI=&itmId=T2+&objL1=41+&objL2=5+10+15+20+25+30+35+40+45+50+55+60+65+70+75+80+85+90+95+100+105+&objL3=&"\
    "objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&"\
    "startPrdDe=202301&endPrdDe=202407&orgId=101&tblId=DT_1B04005N"

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
    df_pop_age = df_pop_age.reset_index(drop=True)
    return df_pop_age

def get_mary_baby_pivot():
    # 3. 경기 혼인건수, 출생아 수 통계
    api_url_mary_baby = "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList"\
    "&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI="\
    "&itmId=T1+&objL1=31+&objL2=10+20+&objL3=&objL4=&objL5=&objL6=&objL7="\
    "&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=202301&endPrdDe=202407&orgId=101&tblId=DT_1B8000G"
    with urlopen(api_url_mary_baby) as url:
        json_file = url.read()
        py_json = json.loads(json_file.decode('utf-8'))
        df_mary_baby = pd.DataFrame(py_json)
    df_mary_baby_pivot = df_mary_baby.pivot_table(index='PRD_DE', columns='C2_NM',values='DT',aggfunc='max').reset_index()
    df_mary_baby_pivot.columns.name = None # 매우 중요
    return df_mary_baby_pivot

def get_employee_pivot():
    # 4. 경기 경제활동인구, 취업, 실업자 수 통계
    api_url_employee ="https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI="\
    "&itmId=T20+T30+T40+&objL1=31+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&"\
    "startPrdDe=202301&endPrdDe=202407&orgId=101&tblId=DT_1DA7004S"

    with urlopen(api_url_employee) as url:
        json_file = url.read()
        py_json = json.loads(json_file.decode('utf-8'))
        df_employee = pd.DataFrame(py_json)
    df_employee_pivot = df_employee.pivot_table(index='PRD_DE', columns='ITM_NM',values='DT',aggfunc='max').reset_index()
    df_employee_pivot['경제활동인구'] = df_employee_pivot['경제활동인구'].astype(float) * 1000
    df_employee_pivot['취업자'] = df_employee_pivot['취업자'].astype(float) * 1000
    df_employee_pivot['실업자'] = df_employee_pivot['실업자'].astype(float) * 1000
    return df_employee_pivot

def get_employee_ratio():
    # 4.2 실업률 통계
    api_url_ratio_employee = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MDE4OWVmZGM1OWNiZWM5ODQ2YWZhMDUyOTIzY2JkNzI=&itmId=T90+&objL1=00+11+31+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=202301&endPrdDe=202407&orgId=101&tblId=DT_1DA7004S'
    with urlopen(api_url_ratio_employee) as url:
        json_file = url.read()
        py_json = json.loads(json_file.decode('utf-8'))
        df_employee_ratio = pd.DataFrame(py_json)
    df_employee_ratio = df_employee_ratio[['PRD_DE','C1_NM','DT']]
    df_employee_ratio['C1_NM'] = df_employee_ratio['C1_NM'].replace('계','전국')
    return df_employee_ratio


# 5. 구인구직통계
# 5.1 전처리 함수 정의
def format_date_recruit(date_str):
    year, month = date_str.split('년 ')
    month = month.replace('월', '')
    return f"{year}{month.zfill(2)}"

def get_recruit():
    # 5.2 통계
    # print('****************현재경로*****************')
    # print(os.getcwd())
    df_recruit = pd.read_excel('/app/volumes/file_volumes/csv/구인구직취업현황(월).xlsx')
    df_recruit = df_recruit.loc[df_recruit['출처']!='총계']
    df_recruit.columns = df_recruit.iloc[12]
    df_recruit = df_recruit.iloc[13:]
    df_recruit['PRD_DE'] = df_recruit['마감년월'].apply(format_date_recruit)
    df_recruit = df_recruit.drop(columns=['마감년월'])
    return df_recruit

# 6. 사업체통계
# 6.1 전처리 함수 정의
def format_date_company(date_str):
    year, month = date_str.split('년')
    month = month.replace('월', '')
    return f"{year}{month.zfill(2)}"

def get_company():
    # 6.2 통계
    df_company = pd.read_excel('/app/volumes/file_volumes/csv/사업장현황(전체).xlsx')
    df_company = df_company.loc[df_company['출처']!='총계']
    df_company.columns = df_company.iloc[12]
    df_company = df_company.iloc[13:]
    df_company['PRD_DE'] = df_company['마감년월'].apply(format_date_company)
    df_company = df_company.drop(columns=['마감년월'])
    return df_company

def get_df_total():
    # 7. Merge
    df_pop_pivot = get_pop_pivot()
    df_mary_baby_pivot = get_mary_baby_pivot()
    df_employee_pivot = get_employee_pivot()
    df_recruit = get_recruit()
    df_company = get_company()

    df_list = [df_pop_pivot,df_mary_baby_pivot,df_employee_pivot,df_recruit,df_company]
    df_total = reduce(lambda x,y : pd.merge(x,y, on='PRD_DE',how='outer'),df_list)
        
    df_final = df_total.rename(columns={"PRD_DE":"PRD_DE",
                                        "남자인구수":"population_male",
                                        "여자인구수":"population_female",
                                        "총인구수":"population_total",
                                        "출생아수(명)":"population_baby",
                                        "혼인건수(건)":"num_married",
                                        "경제활동인구":"population_economic",
                                        "실업자":"population_unemployed",
                                        "취업자":"population_employed",
                                        "구인인원(월)":"population_job_open",
                                        "구직건수(월)":"num_job_search",
                                        "취업건수(월)":"num_employed",
                                        "사업장수(전체)":"num_company"
                                        })
    df_final = df_final.fillna(0)
    
    return df_final


def check_table(db_connect,table_name):

    check_table_query = f"""
    SELECT EXISTS (
        SELECT FROM pg_tables
        WHERE tablename = '{table_name}'
    );
    """
    with db_connect.cursor() as cur:
        cur.execute(check_table_query)
        result = cur.fetchone()[0]
    return result    

def make_total_table(db_connect):

    create_table_query = """
    CREATE TABLE IF NOT EXISTS gjf_total_data (
        INDEX SERIAL PRIMARY KEY,
        PRD_DE CHAR(6),
        population_male int,
        population_female int,
        population_total int,
        population_baby int,
        num_married int,
        population_economic int,
        population_unemployed int,
        population_employed int,
        population_job_open int,
        num_job_search int,
        num_employed int,
        num_company int   
    );
    """
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()
        print("TOTAL TABLE CREATION IS SUCCESSFUL")

def make_pop_comp_table(db_connect):

    create_table_query = """
    CREATE TABLE IF NOT EXISTS gjf_pop_comp_data (
        INDEX SERIAL PRIMARY KEY,
        PRD_DE CHAR(6),
        DT INT,
        C1_NM VARCHAR
    );
    """
    #print(create_table_query)
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()
        print("POP COMP TABLE CREATION IS SUCCESSFUL")

def make_pop_age_table(db_connect):

    create_table_query = """
    CREATE TABLE IF NOT EXISTS gjf_pop_age_data (
        INDEX SERIAL PRIMARY KEY,
        PRD_DE CHAR(6),
        AGE_GRP VARCHAR,
        DT INT
    );
    """
    #print(create_table_query)
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()
        print("POP AGE TABLE CREATION IS SUCCESSFUL")

def make_employee_ratio_table(db_connect):

    create_table_query = """
    CREATE TABLE IF NOT EXISTS gjf_employee_ratio_data (
        INDEX SERIAL PRIMARY KEY,
        PRD_DE CHAR(6),
        C1_NM VARCHAR,
        DT FLOAT(8)
    );
    """
    #print(create_table_query)
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()
        print("EMPLOYEE RATIO TABLE CREATION IS SUCCESSFUL")


def insert_total_data(db_connect,data):
    for i in range(len(data)):
        insert_row_query = f"""
        INSERT INTO gjf_total_data(
        PRD_DE,
        population_male,
        population_female,
        population_total,
        population_baby,
        num_married,
        population_economic,
        population_unemployed,
        population_employed,
        population_job_open,
        num_job_search,
        num_employed,
        num_company)
            VALUES (
            {data.PRD_DE.iloc[i]},
            {data.population_male.iloc[i]},
            {data.population_female.iloc[i]},
            {data.population_total.iloc[i]},
            {data.population_baby.iloc[i]},
            {data.num_married.iloc[i]},
            {data.population_economic.iloc[i]},
            {data.population_unemployed.iloc[i]},
            {data.population_employed.iloc[i]},
            {data.population_job_open.iloc[i]},
            {data.num_job_search.iloc[i]},
            {data.num_employed.iloc[i]},
            {data.num_company.iloc[i]}
            );"""

        with db_connect.cursor() as cur:
            cur.execute(insert_row_query)
            db_connect.commit()
    print("TOTAL DATA INSERTION IS SUCCESSFUL")

def insert_pop_comp_data(db_connect,data):
    for i in range(len(data)):
        insert_row_query = f"""
        INSERT INTO gjf_pop_comp_data(
        PRD_DE,
        DT,
        C1_NM)
            VALUES (
            {data.PRD_DE.iloc[i]},
            {data.DT.iloc[i]},
            '{data.C1_NM.iloc[i]}'
            );"""

        with db_connect.cursor() as cur:
            cur.execute(insert_row_query)
            db_connect.commit()
    print("POP_COMP DATA INSERTION IS SUCCESSFUL")

def insert_pop_age_data(db_connect,data):
    for i in range(len(data)):
        insert_row_query = f"""
        INSERT INTO gjf_pop_age_data(
        PRD_DE,
        AGE_GRP,
        DT)
            VALUES (
            {data.PRD_DE.iloc[i]},
            '{data.AGE_GRP.iloc[i]}',
            {data.DT.iloc[i]}
            );"""

        with db_connect.cursor() as cur:
            cur.execute(insert_row_query)
            db_connect.commit()
    print("POP AGE DATA INSERTION IS SUCCESSFUL")

def insert_employee_ratio_data(db_connect,data):
    for i in range(len(data)):
        insert_row_query = f"""
        INSERT INTO gjf_employee_ratio_data(
        PRD_DE,
        C1_NM,
        DT)
            VALUES (
            {data.PRD_DE.iloc[i]},
            '{data.C1_NM.iloc[i]}',
            {data.DT.iloc[i]}
            );"""

        with db_connect.cursor() as cur:
            cur.execute(insert_row_query)
            db_connect.commit()
    print("EMPLOYEE RATIO DATA INSERTION IS SUCCESSFUL")

if __name__ == "__main__":
    #if 체크 만들기
    db_connect = psycopg2.connect(
        user="postgres_user",
        password="postgres_password",
        host="postgres_server",
        port=5432,
        database="postgres_db"
    )
    if not check_table(db_connect,"gjf_total_data"):
        make_total_table(db_connect)
        df = get_df_total()
        insert_total_data(db_connect,df)

    if not check_table(db_connect,"gjf_pop_comp_data"):
        make_pop_comp_table(db_connect)
        df = get_pop_comp()
        insert_pop_comp_data(db_connect,df)

    if not check_table(db_connect,"gjf_pop_age_data"):
        make_pop_age_table(db_connect)
        df = get_pop_age()
        insert_pop_age_data(db_connect,df)

    if not check_table(db_connect,"gjf_employee_ratio_data"):
        make_employee_ratio_table(db_connect)
        df = get_employee_ratio()
        insert_employee_ratio_data(db_connect,df)
    
    db_connect.close()