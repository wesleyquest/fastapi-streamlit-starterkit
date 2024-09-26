import psycopg2

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
