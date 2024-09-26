#import packages
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import psycopg2
import pandas.io.sql as psql

@st.cache_data(show_spinner=False)
def load_data():
    # postgres에서 가져오기
    # fmf_schedule_file_path = "/app/src/data/production_plan_htc/production_plan_htc_202406.csv" 
    # grade_info_file_path = "/app/src/data/production_plan_htc/grade_info.csv"
    # fmf_schedule = pd.read_csv(fmf_schedule_file_path)
    # grade_info = pd.read_csv(grade_info_file_path)

    db_connect = psycopg2.connect(
        user="postgres_user",
        password="postgres_password",
        host="postgres_server",
        port=5432,
        database="postgres_db"
    )

    fmf_schedule = psql.read_sql_query("SELECT * FROM production_plan_htc_202406_data",db_connect)
    grade_info = psql.read_sql_query("SELECT * FROM grade_info_data",db_connect)
    db_connect.close()
    return fmf_schedule, grade_info

#create df_fmf_main
def create_df_fmf_main(fmf_schedule, grade_info):
    
    # Step 1: Drop columns 1 through 10, but keep the 'Total' row
    df_processed = fmf_schedule.drop(fmf_schedule.columns[1:10], axis=1)
    
    # Step 2: Clean the 'GRADE' column
    df_processed.iloc[:, 0] = df_processed.iloc[:, 0].str.replace('/SN', '')
    
    # Step 3: Separate the 'Total' row for later use
    total_row = df_processed[df_processed['GRADE'].str.strip().str.lower() == 'total']
    
    # Step 4: Remove the 'Total' row from the main dataset
    df_processed = df_processed[df_processed['GRADE'].str.strip().str.lower() != 'total']
    
    # Step 5: Melt the DataFrame to convert it from wide to long format
    df_long = df_processed.melt(id_vars=['GRADE'], var_name='Day', value_name='Production')
    
    # Step 6: Convert Day to numeric, coercing errors to NaN, then drop NaN rows
    ##in snowflake : df_long["Day"] = df_long["Day"].str.split("_").str[1].astype(int)
    df_long['Day'] = pd.to_numeric(df_long['Day'], errors='coerce')
    df_long = df_long.dropna(subset=['Day'])
    
    # Step 7: Filter out invalid days (only 1 through 30 for June)
    df_long = df_long[(df_long['Day'] >= 1) & (df_long['Day'] <= 30)]
    
    # Step 8: Add Year and Month columns with values 2024 and 06
    df_long['Year'] = 2024
    df_long['Month'] = 6
    
    # Step 9: Create the 'Date' column by combining Year, Month, and Day
    df_long['Date'] = pd.to_datetime(df_long[['Year', 'Month', 'Day']])
    
    # Drop the 'Year', 'Month', and 'Day' columns if they are no longer needed
    df_long.drop(columns=['Year', 'Month', 'Day'], inplace=True)
    
    # Step 10: Convert the Production column to numeric, handling commas
    df_long['Production'] = df_long['Production'].replace(',', '', regex=True).astype(float)
    
    # Step 11: Filter out rows where Production is zero or NaN
    df_long = df_long[df_long['Production'] > 0]
    
    # Step 12: Sort by Date and GRADE to ensure proper ordering
    df_long = df_long.sort_values(by=['Date', 'GRADE'])
    
    # Step 13: Identify FMF and OG grades
    fmf_grades = ['BI770', 'BI871', 'BI870', 'BI873', 'BI991', 'BI997']
    og_grades = ['PPOG/S', 'PROG/S']
    
    df_long['FMF'] = df_long['GRADE'].apply(lambda x: 'FMF' if x in fmf_grades else '')
    df_long['OG'] = df_long['GRADE'].apply(lambda x: 'OG' if x in og_grades else '')

    # Step 14: Identify the start and end dates of FMF grade production
    fmf_start_date = df_long[df_long['FMF'] == 'FMF']['Date'].min() - pd.Timedelta(days=1)
    fmf_end_date = df_long[df_long['FMF'] == 'FMF']['Date'].max() + pd.Timedelta(days=1)
    
    # Step 15: Filter the DataFrame to include only the range from 6/15 to 6/20
    fmf_df = df_long[(df_long['Date'] >= fmf_start_date) & (df_long['Date'] <= fmf_end_date)]
    
    # Step 16: Sort the filtered DataFrame by Date and GRADE
    fmf_df_sorted = fmf_df.sort_values(by=['Date', 'GRADE']).reset_index(drop=True)
    
    # Step 17: Reorder FMF grades
    def reorder_fmf_start_end(df):
        df_sorted = df.sort_values(by=['Date', 'GRADE']).reset_index(drop=True)
    
        fmf_start_date = df_sorted[df_sorted['FMF'] == 'FMF']['Date'].min()
        fmf_end_date = df_sorted[df_sorted['FMF'] == 'FMF']['Date'].max()
    
        def adjust_fmf_within_date(group):
            fmf = group[group['FMF'] == 'FMF']
            non_fmf = group[group['FMF'] != 'FMF']
    
            if group['Date'].iloc[0] == fmf_start_date:
                return pd.concat([non_fmf, fmf])
            elif group['Date'].iloc[0] == fmf_end_date:
                return pd.concat([fmf, non_fmf])
            else:
                return pd.concat([non_fmf, fmf])
    
        df_adjusted = df_sorted.groupby('Date', group_keys=False).apply(adjust_fmf_within_date).reset_index(drop=True)
    
        return df_adjusted
    
    df_fmf_final_adjusted = reorder_fmf_start_end(fmf_df_sorted)

    # Step 18: Reorder OG grades around FMF grades
    def adjust_og_placement_without_changing_fmf_order(df):
        fmf_start_index = df[df['FMF'] == 'FMF'].index.min()
        fmf_end_index = df[df['FMF'] == 'FMF'].index.max()
        og_indices = df[df['OG'] == 'OG'].index
    
        first_og_index = og_indices[og_indices < fmf_start_index].max() if not og_indices[og_indices < fmf_start_index].empty else None
        last_og_index = og_indices[og_indices > fmf_end_index].min() if not og_indices[og_indices > fmf_end_index].empty else None
    
        df_adjusted = df.copy()
    
        if last_og_index is not None:
            og_row = df_adjusted.loc[last_og_index]
            df_adjusted = df_adjusted.drop(last_og_index)
            df_adjusted = pd.concat([df_adjusted.iloc[:fmf_end_index + 1], pd.DataFrame([og_row]), df_adjusted.iloc[fmf_end_index + 1:]]).reset_index(drop=True)
    
        return df_adjusted
    
    df_fmf_final_with_og_adjusted = adjust_og_placement_without_changing_fmf_order(df_fmf_final_adjusted)

    # Step 19: Calculate Start and End times based on production proportions
    
    # Ensure the GRADE order is preserved
    df_fmf_final_with_og_adjusted['GRADE'] = pd.Categorical(df_fmf_final_with_og_adjusted['GRADE'], ordered=True)
    
    # Initialize Start times to midnight (00:00) for each date
    df_fmf_final_with_og_adjusted['Start'] = df_fmf_final_with_og_adjusted['Date']

    # Calculate Duration as a proportion of the total daily production
    total_production_by_date = df_fmf_final_with_og_adjusted.groupby('Date')['Production'].sum()
    df_fmf_final_with_og_adjusted = df_fmf_final_with_og_adjusted.merge(total_production_by_date, on='Date', suffixes=('', '_Total'))
    
    df_fmf_final_with_og_adjusted['Duration'] = (
        df_fmf_final_with_og_adjusted['Production'] / df_fmf_final_with_og_adjusted['Production_Total']
    ) * pd.Timedelta(hours=24)

    df_fmf_final_with_og_adjusted["End"] = df_fmf_final_with_og_adjusted["Start"][0] + df_fmf_final_with_og_adjusted['Duration'].cumsum()
    df_fmf_final_with_og_adjusted["Start"] = df_fmf_final_with_og_adjusted["End"] - df_fmf_final_with_og_adjusted['Duration']
    
    df_fmf_final_with_og_adjusted["Start"] = df_fmf_final_with_og_adjusted["Start"].dt.floor('min')
    df_fmf_final_with_og_adjusted["End"] = df_fmf_final_with_og_adjusted["End"].dt.floor('min')
    df_fmf_final_with_og_adjusted.drop(columns=['Production_Total', "Date"], inplace=True)
    ###############################################################################################
    # Organize the schedule (df name : smp_{number})
    df_fmf_final_with_og_adjusted.loc[(df_fmf_final_with_og_adjusted["Start"]<=df_fmf_final_with_og_adjusted[df_fmf_final_with_og_adjusted['FMF'] == 'FMF']['Start'].min()) & (df_fmf_final_with_og_adjusted["OG"]=="OG"), "OG"] = "OG before"
    df_fmf_final_with_og_adjusted.loc[(df_fmf_final_with_og_adjusted["Start"]>=df_fmf_final_with_og_adjusted[df_fmf_final_with_og_adjusted['FMF'] == 'FMF']['End'].max()) & (df_fmf_final_with_og_adjusted["OG"]=="OG"), "OG"] = "OG after"

    smp_1 = df_fmf_final_with_og_adjusted.groupby(["GRADE","FMF","OG"], as_index=False, observed=False)[["Production","Duration"]].sum()
    smp_1 = smp_1[smp_1["Production"]>0]
    smp_2 = df_fmf_final_with_og_adjusted.sort_values(by="Start", ascending=True).drop_duplicates(["GRADE","FMF","OG"])[["GRADE","FMF","OG","Start"]]
    
    df_fmf_final = pd.merge(smp_1, smp_2, on=["GRADE","FMF","OG"], how="inner").sort_values(by="Start", ascending=True).reset_index(drop=True)
    df_fmf_final["End"] = ""
    df_fmf_final["End"] = df_fmf_final["Start"][0] + df_fmf_final['Duration'].cumsum()
    df_fmf_final["Start"] = df_fmf_final["End"] - df_fmf_final['Duration']
    df_fmf_final["Start"] = pd.to_datetime(df_fmf_final["Start"]).dt.floor('min')
    df_fmf_final["End"] = pd.to_datetime(df_fmf_final["End"]).dt.floor('min')
    df_fmf_final["GRADE"] = df_fmf_final["GRADE"].astype(str)
    df_fmf_final["Production"] = df_fmf_final["Production"].astype(int).astype(str)

    grade_info.iloc[:, 0] = grade_info.iloc[:, 0].str.replace('/SN', '')
    df_fmf_final = pd.merge(df_fmf_final, grade_info, on="GRADE", how="left")
    df_fmf_final["INFO"] = df_fmf_final["INFO"].fillna("")

    return df_fmf_final

#create df_fmf_quality
def create_df_fmf_quality(df_fmf_main):

    range_x=[pd.Timestamp(min(df_fmf_main["Start"]).strftime('%Y-%m-%d')),
             pd.Timestamp((max(df_fmf_main["End"]) + pd.Timedelta(1,"d")).strftime('%Y-%m-%d'))]
    range_x_before_fmf = [min(df_fmf_main["Start"]).round("h"), min(df_fmf_main[df_fmf_main["FMF"]=="FMF"]["Start"]).round("h")]
    range_x_fmf = [min(df_fmf_main[df_fmf_main["FMF"]=="FMF"]["Start"]).round("h"), max(df_fmf_main[df_fmf_main["FMF"]=="FMF"]["End"]).round("h")]
    range_x_after_fmf = [max(df_fmf_main[df_fmf_main["FMF"]=="FMF"]["End"]).round("h"), max(df_fmf_main["End"]).round("h")]

    def make_range_even(range_list):
        for i,v in enumerate(range_list):
            if int(v.strftime("%H"))%2!=0:
                range_list[i] = v + pd.Timedelta(1, "h")
    
    make_range_even(range_x_before_fmf)
    make_range_even(range_x_fmf)
    make_range_even(range_x_after_fmf)
    
    def create_quality_period(name, range_x_before_fmf, range_x_fmf, range_x_after_fmf, non_fmf_period, fmf_period):
        #range_x_before_fmf
        df_range_x_before_fmf = pd.DataFrame({"Period":pd.date_range(range_x_before_fmf[0], range_x_before_fmf[1],  freq=non_fmf_period)})
        #range_x_fmf
        df_range_x_fmf = pd.DataFrame({"Period":pd.date_range(range_x_fmf[0], range_x_fmf[1],  freq=fmf_period)})
        #range_x_after_fmf
        df_range_x_after_fmf = pd.DataFrame({"Period":pd.date_range(range_x_after_fmf[0], range_x_after_fmf[1],  freq=non_fmf_period)})
        
        df = pd.concat([df_range_x_before_fmf, df_range_x_fmf, df_range_x_after_fmf])
        df["Quality"] = name
        
        return df

    MI = create_quality_period("1. MI", range_x_before_fmf, range_x_fmf, range_x_after_fmf, "4h", "4h")
    B_C2 = create_quality_period("2. B-C2", range_x_before_fmf, range_x_fmf, range_x_after_fmf, "4h", "4h")
    X_S = create_quality_period("3. X.S", range_x_before_fmf, range_x_fmf, range_x_after_fmf, "8h", "8h")
    I_V = create_quality_period("4. I.V", range_x_before_fmf, range_x_fmf, range_x_after_fmf, "8h", "8h")
    
    quality_period = pd.concat([MI, B_C2, X_S, I_V]).reset_index(drop=True)
    ##quality_period = quality_period[quality_period["Period"]!=range_x[0]]

    quality_period.loc[(quality_period["Period"]>=df_fmf_main[df_fmf_main['OG'] == 'OG before']['Start'].min())&(quality_period["Period"]<=df_fmf_main[df_fmf_main['OG'] == 'OG before']['End'].max()), "Class"] = "OG"
    quality_period.loc[(quality_period["Period"]>=df_fmf_main[df_fmf_main['OG'] == 'OG after']['Start'].min())&(quality_period["Period"]<=df_fmf_main[df_fmf_main['OG'] == 'OG after']['End'].max()), "Class"] = "OG"
    quality_period.loc[(quality_period["Period"]>=df_fmf_main[df_fmf_main['FMF'] == 'FMF']['Start'].min())&(quality_period["Period"]<=df_fmf_main[df_fmf_main['FMF'] == 'FMF']['End'].max()), "Class"] = "FMF"
    quality_period["Class"] = quality_period["Class"].fillna("Non-FMF")

    #additional_quality_check : B-2C, X.S/I.V
    def check_additional_period(x, quality, df_fmf_main, period_hour_int):
        #grade current
        grade_current = df_fmf_main[(df_fmf_main["Start"] <= (x))&(df_fmf_main["End"] >= (x))]
        grade_current = grade_current.sort_values(by="End", ascending=False).reset_index(drop=True)["GRADE"][0]
        #grade before
        try:
            grade_before = df_fmf_main[(df_fmf_main["Start"] <= (x - pd.Timedelta(period_hour_int, "h")))&(df_fmf_main["End"] >= (x - pd.Timedelta(period_hour_int, "h")))]
            grade_before = grade_before.sort_values(by="End", ascending=False).reset_index(drop=True)["GRADE"][0]
            if grade_before != grade_current:
                return quality
        except:
            return quality

    B_C2_add = pd.DataFrame({"Period":pd.date_range(range_x_fmf[0], range_x_fmf[1],  freq="2h")})
    B_C2_add["Quality"] = B_C2_add["Period"].apply(check_additional_period,
                                                   df_fmf_main=df_fmf_main,
                                                   quality="2. B-C2",
                                                   period_hour_int=4)
    X_S_add = pd.DataFrame({"Period":pd.date_range(range_x_fmf[0], range_x_fmf[1],  freq="4h")})
    X_S_add["Quality"] = X_S_add["Period"].apply(check_additional_period,
                                                   df_fmf_main=df_fmf_main,
                                                   quality="3. X.S",
                                                   period_hour_int=6)
    I_V_add = pd.DataFrame({"Period":pd.date_range(range_x_fmf[0], range_x_fmf[1],  freq="4h")})
    I_V_add["Quality"] = I_V_add["Period"].apply(check_additional_period,
                                                   df_fmf_main=df_fmf_main,
                                                   quality="4. I.V",
                                                   period_hour_int=6)
    
    additional_quality_period = pd.concat([B_C2_add, X_S_add, I_V_add]).reset_index(drop=True)
    additional_quality_period = additional_quality_period.dropna(subset="Quality")
    additional_quality_period["Class"] = "Grade Change"

    quality_period_final = pd.concat([quality_period, additional_quality_period]).drop_duplicates(["Period", "Quality"])

    return quality_period_final

def check_additional_period(x, quality, df_fmf_main, period_hour_int):
    #grade current
    grade_current = df_fmf_main[(df_fmf_main["Start"] <= (x))&(df_fmf_main["End"] >= (x))]
    grade_current = grade_current.sort_values(by="End", ascending=False).reset_index(drop=True)["GRADE"][0]
    #grade before
    try:
        grade_before = df_fmf_main[(df_fmf_main["Start"] <= (x - pd.Timedelta(period_hour_int, "h")))&(df_fmf_main["End"] >= (x - pd.Timedelta(period_hour_int, "h")))]
        grade_before = grade_before.sort_values(by="End", ascending=False).reset_index(drop=True)["GRADE"][0]
        if grade_before != grade_current:
            return quality
    except:
        return quality

