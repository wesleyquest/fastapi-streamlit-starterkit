#import packages
import numpy as np
import pandas as pd
import streamlit as st
import psycopg2
import pandas.io.sql as psql

@st.cache_data(show_spinner=False)
def load_data():
    # postgres에서 가져오기
    #file_path = "/app/src/data/glossary_htc/glossary_htc.csv"
    #df = pd.read_csv(file_path)

    db_connect = psycopg2.connect(
            user="postgres_user",
            password="postgres_password",
            host="postgres_server",
            port=5432,
            database="postgres_db"
        )

    df = psql.read_sql_query("SELECT * FROM glossary_htc_data",db_connect)
    db_connect.close()
    return df

def make_glossary_terms(df):

    for i in df.columns:
        df[i] = df[i].astype("str")

    df_plant = df[["PLANT_CODE", "PLANT_DESC"]]
    df_plant["HIERARCHY"] = df_plant["PLANT_CODE"]
    df_plant["CLASS"] = "PLANT"
    df_plant = df_plant.drop_duplicates(subset="HIERARCHY").reset_index(drop=True)
    df_plant = df_plant[["PLANT_CODE", "CLASS" ,"HIERARCHY", "PLANT_DESC"]]
    df_plant.columns = ["CODE", "CLASS", "HIERARCHY", "DESC"]
    
    df_unit = df[["UNIT_CODE", "UNIT_DESC", "PLANT_CODE"]]
    df_unit["HIERARCHY"] = df_unit["PLANT_CODE"] + " > " + df_unit["UNIT_CODE"]
    df_unit["CLASS"] = "UNIT"
    df_unit = df_unit.drop_duplicates(subset="HIERARCHY").reset_index(drop=True)
    df_unit = df_unit[["UNIT_CODE", "CLASS", "HIERARCHY", "UNIT_DESC"]]
    df_unit.columns = ["CODE", "CLASS", "HIERARCHY", "DESC"]
    
    df_eqp = df[["EQP_CODE", "EQP_TYPE", "EQP_DESC", "PLANT_CODE", "UNIT_CODE"]]
    df_eqp["HIERARCHY"] = df_eqp["PLANT_CODE"] + " > " + df_eqp["UNIT_CODE"] + " > " + df_eqp["EQP_CODE"]
    df_eqp["CLASS"] = "EQP"
    df_eqp = df_eqp.drop_duplicates(subset="HIERARCHY").reset_index(drop=True)
    df_eqp = df_eqp[["EQP_CODE", "CLASS", "HIERARCHY", "EQP_TYPE", "EQP_DESC"]]
    df_eqp.columns = ["CODE", "CLASS", "HIERARCHY", "TYPE", "DESC"]
    
    df_sub_eqp = df[["SUB_EQP_CODE", "SUB_EQP_TYPE", "SUB_EQP_DESC", "PLANT_CODE", "UNIT_CODE", "EQP_CODE"]]
    df_sub_eqp["HIERARCHY"] = df_sub_eqp["PLANT_CODE"] + " > " + df_sub_eqp["UNIT_CODE"] + " > " + df_sub_eqp["EQP_CODE"] + " > " + df_sub_eqp["SUB_EQP_CODE"]
    df_sub_eqp["CLASS"] = "SUB_EQP"
    df_sub_eqp = df_sub_eqp.drop_duplicates(subset="HIERARCHY").reset_index(drop=True)
    df_sub_eqp = df_sub_eqp[["SUB_EQP_CODE", "CLASS", "HIERARCHY", "SUB_EQP_TYPE", "SUB_EQP_DESC"]]
    df_sub_eqp.columns = ["CODE", "CLASS", "HIERARCHY", "TYPE", "DESC"]
    
    df_oper = df[["OPER_CODE", "OPER_TYPE", "DATA_TYPE", "OPER_DESC", "PLANT_CODE", "UNIT_CODE", "EQP_CODE", "SUB_EQP_CODE"]]
    df_oper["HIERARCHY"] = df_oper["PLANT_CODE"] + " > " + df_oper["UNIT_CODE"] + " > " + df_oper["EQP_CODE"] + " > " + df_oper["SUB_EQP_CODE"] + " > " + df_oper["OPER_CODE"]
    df_oper["CLASS"] = "OPER"
    df_oper = df_oper.drop_duplicates(subset="HIERARCHY").reset_index(drop=True)
    df_oper = df_oper[["OPER_CODE", "CLASS", "HIERARCHY", "OPER_TYPE", "DATA_TYPE", "OPER_DESC"]]
    df_oper.columns = ["CODE", "CLASS", "HIERARCHY", "TYPE", "DATA_TYPE" ,"DESC"]
    
    df_1 = pd.concat([df_plant, df_unit, df_eqp, df_sub_eqp, df_oper]).reset_index(drop=True)
    
    return df_1

def split_frame(input_df, rows):
    #df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    df = [input_df.loc[i+1 : i + rows, :] for i in range(0, len(input_df), rows)]
    return df




