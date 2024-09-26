from src.gjf.create_table import check_table, make_total_table, make_pop_comp_table, make_pop_age_table, make_employee_ratio_table
from src.gjf.preprocessing_data import get_df_total, get_pop_comp, get_pop_age, get_employee_ratio
from src.gjf.insert_data import insert_total_data, insert_pop_comp_data, insert_pop_age_data, insert_employee_ratio_data
import psycopg2

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