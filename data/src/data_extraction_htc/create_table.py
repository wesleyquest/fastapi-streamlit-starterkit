import pandas as pd
import psycopg2

def create_table_from_csv(db_connect, df, table_name):

    columns = []
    for col, dtype in zip(df.columns, df.dtypes):
        if dtype == 'int64':
            col_type = 'BIGINT'
        elif dtype == 'float64':
            col_type = 'FLOAT'
        else:
            col_type = 'TEXT'
        columns.append(f'"{col}" {col_type}')

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(columns)}
    );
    """

    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()
        print(f"Table {table_name} creation is successful.")

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
