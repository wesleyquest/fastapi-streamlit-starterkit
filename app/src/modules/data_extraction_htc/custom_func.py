import pandas as pd


#functions
##ois
def read_ois_table(start_date, end_date, target_tag):
    start_date = start_date + "000000"
    end_date = end_date + "000000"
    df = pd.read_csv("/app/src/data/data_extraction_htc/ois_table.csv", dtype={"EVENT_TIME":object})
    df = df[(df["EVENT_TIME"] >= start_date) & (df["EVENT_TIME"] <= end_date)]
    df = df[df["TAG_NAME"].isin(target_tag)]
    return df

##lims
def read_lims_table(start_date, end_date, sample_point, item_name):
    start_date = start_date + "000000"
    end_date = end_date + "000000"
    df = pd.read_csv("/app/src/data/data_extraction_htc/lims_table.csv", dtype={"SAMPLING_DATE":object})
    df = df[(df["SAMPLING_DATE"] >= start_date) & (df["SAMPLING_DATE"] <= end_date)]
    df = df[df["SAMPLE_POINT"]==sample_point]
    df = df[df["ITEM_NAME"].isin(item_name)]
    return df


def set_freq(time_unit):
    if time_unit[-1] == "Y" or time_unit[-1] == "M":
        return time_unit + "S"
    return time_unit

def beautify_columns(df, date_column, time_unit):
    if time_unit[-1] == "Y":
        df["DATE"] = df[date_column].dt.strftime("%Y")
        df = df[["DATE"] + [col for col in df.columns if col !="DATE"]]
    elif time_unit[-1] == "M":
        df["DATE"] = df[date_column].dt.strftime("%Y-%m")
        df = df[["DATE"] + [col for col in df.columns if col !="DATE"]]
    elif time_unit[-1] == "d":
        df["DATE"] = df[date_column].dt.strftime("%Y-%m-%d")
        df = df[["DATE"] + [col for col in df.columns if col !="DATE"]]
    else:
        df["DATE"] = df[date_column].dt.strftime("%Y-%m-%d")
        df["TIME"] = df[date_column].dt.strftime("%H:%M:%S")
        df = df[["DATE", "TIME"] + [col for col in df.columns if col !="DATE" and col != "TIME"]]
    
    return df



def transform_ois_data(df, date_column, time_unit):
    freq = set_freq(time_unit)
    df[date_column] = pd.to_datetime(df[date_column], format='%Y%m%d%H%M%S', errors='coerce')
    df = pd.DataFrame(df.groupby([pd.Grouper(key=date_column, freq=freq, dropna=False), pd.Grouper("TAG_NAME")])["VALUE"].mean()).reset_index().rename_axis(None, axis=1)
    df = pd.pivot_table(df, values='VALUE', index=[date_column],columns=['TAG_NAME'], aggfunc="mean", fill_value=0).reset_index().rename_axis(None, axis=1)
    df = beautify_columns(df, date_column, time_unit)
    df = df.drop(date_column, axis=1)
    return df

def convert_data_type_char_result(x):
    try:
        return float(x)
    except:
        return 0

def transform_lims_data(df, date_column, time_unit):
    freq = set_freq(time_unit)
    #CHAR RESULT 값을 FLOAT형태로 변경하며, 변경되지 못하는 값은 0으로 반환합니다.
    df["CHAR_RESULT"] = df["CHAR_RESULT"].apply(convert_data_type_char_result)
    df = df.rename(columns = {'CHAR_RESULT' : 'VALUE'})
    df[date_column] = pd.to_datetime(df[date_column], format='%Y%m%d%H%M%S', errors='coerce')
    df = pd.DataFrame(df.groupby(pd.Grouper(key=date_column, freq=freq, dropna=False))["VALUE"].sum()).reset_index().rename_axis(None, axis=1)
    df = beautify_columns(df, date_column, time_unit)
    df = df.drop(date_column, axis=1)
    
    return df