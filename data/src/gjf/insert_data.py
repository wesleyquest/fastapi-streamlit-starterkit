import psycopg2

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
