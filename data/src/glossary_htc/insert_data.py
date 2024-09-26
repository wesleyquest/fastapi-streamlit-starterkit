import pandas as pd
from psycopg2 import extras

def sanitize_column_name(column_name):
    return f'"{column_name}"'  # 쌍따옴표로 감싸기


def insert_data_from_csv(db_connect, df, table_name):

    columns = [', '.join([sanitize_column_name(col) for col in df.columns])]

    insert_data_query = f"""
    INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s
    """
    tuples = [tuple(x) for x in df.to_numpy()]

    with db_connect.cursor() as cur:
        extras.execute_values(cur,insert_data_query,tuples)
        db_connect.commit()
        print(f"Data insertion into {table_name} is successful.")

