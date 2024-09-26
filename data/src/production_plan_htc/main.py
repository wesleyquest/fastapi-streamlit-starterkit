from src.production_plan_htc.create_table import create_table_from_csv, check_table
from src.production_plan_htc.insert_data import insert_data_from_csv
import psycopg2
import pandas as pd

if __name__ == "__main__":
    #if 체크 만들기
    db_connect = psycopg2.connect(
        user="postgres_user",
        password="postgres_password",
        host="postgres_server",
        port=5432,
        database="postgres_db"
    )
    grade_info_df = pd.read_csv("/app/volumes/file_volumes/production_plan_htc/grade_info.csv")
    production_plan_htc_202405_df = pd.read_csv("/app/volumes/file_volumes/production_plan_htc/production_plan_htc_202405.csv")
    production_plan_htc_202406_df = pd.read_csv("/app/volumes/file_volumes/production_plan_htc/production_plan_htc_202406.csv")
    if not check_table(db_connect,"grade_info_data"):
        create_table_from_csv(db_connect,grade_info_df, "grade_info_data")
        insert_data_from_csv(db_connect,grade_info_df, "grade_info_data")

    if not check_table(db_connect, "production_plan_htc_202405_data"):
        create_table_from_csv(db_connect, production_plan_htc_202405_df, "production_plan_htc_202405_data")
        insert_data_from_csv(db_connect, production_plan_htc_202405_df, "production_plan_htc_202405_data")

    if not check_table(db_connect, "production_plan_htc_202406_data"):
        create_table_from_csv(db_connect, production_plan_htc_202406_df, "production_plan_htc_202406_data")
        insert_data_from_csv(db_connect, production_plan_htc_202406_df, "production_plan_htc_202406_data")

    db_connect.close()