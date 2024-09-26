from src.data_extraction_htc.create_table import create_table_from_csv, check_table
from src.data_extraction_htc.insert_data import insert_data_from_csv
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
    lims_df = pd.read_csv("/app/volumes/file_volumes/data_extraction_htc/lims_table.csv")
    ois_df = pd.read_csv("/app/volumes/file_volumes/data_extraction_htc/ois_table.csv")
    if not check_table(db_connect,"limbs_data"):
        create_table_from_csv(db_connect,lims_df, "limbs_data")
        insert_data_from_csv(db_connect,lims_df, "limbs_data")

    if not check_table(db_connect, "ois_data"):
        create_table_from_csv(db_connect, ois_df, "ois_data")
        insert_data_from_csv(db_connect, ois_df, "ois_data")

    db_connect.close()