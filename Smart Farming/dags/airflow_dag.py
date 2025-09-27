# ---------------------------------------------------------
# Airflow Code
# ---------------------------------------------------------

'''

In this script, we 

'''


# -----------------
# load libraries
# -----------------

from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import sys
import pandas as pd
from datetime import datetime, timedelta



# -----------------
# API data load
# -----------------

# --------------------------------------------------------
# Extract standard weather data: using VisualCrossing
# --------------------------------------------------------



def std_data_extract(data):

    response_standard_data = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Rotterdam?unitGroup=us&key=XTJF7TPU48LF8YN9TXGMG7C8N&contentType=json&include=days")
    if response_standard_data.status_code!=200:
        print('Unexpected Status code: ', response_standard_data.status_code)
        sys.exit()  


    # Parse the results as JSON
    data = response_standard_data.json()

    df_std = pd.json_normalize(data['days'])
    
    df_std['location'] = data['resolvedAddress']
    df_std['latitude'] = data['latitude']
    df_std['longitude'] = data['longitude']
    
    if 'hours' in df_std.columns:
        df_std = df_std.drop('hours', axis=1)
    
    return df_std




# --------------------------------------------------------
# Extract agricultural data: using stormglass.io
# --------------------------------------------------------


def agri_data_extract(agri_data):

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    response = requests.get(
    'https://api.stormglass.io/v2/bio/point',
    params={
        'lat': 51.9144,
        'lng': 4.48717,
        'params': ','.join(['soilMoisture', 'soilMoisture10cm', 'soilMoisture40cm', 'soilTemperature', 'soilTemperature10cm', 'soilTemperature40cm']),
        'start': start_timestamp,  
        'end': end_timestamp 
    },
    headers={
        'Authorization': '9915000e-63c0-11f0-976d-0242ac130006-99150068-63c0-11f0-976d-0242ac130006'
    }
    )

    json_data = response.json()

    df_agri = pd.json_normalize(json_data['hours'])
    df_agri['time'] = pd.to_datetime(df_agri['time'])

    return df_agri



# -----------------
# Data Cleaning & Transformation 
# -----------------


def prep_std_data(df_std):

    df_std['datetime'] = pd.to_datetime(df_std['datetime'])
    df_std['day_name'] = df_std['datetime'].dt.day_name()

    return df_std


def prep_agri_data(df_agri):

    df_agri['time'] = df_agri['time'].dt.tz_localize(None)

    df_agri_daily = df_agri.copy()

    df_agri['day_name'] = df_agri['time'].dt.day_name()

    df_agri_daily = df_agri_daily.groupby(pd.Grouper(key='time', freq='D')).mean().round(3).reset_index()
    df_agri_daily['day_name'] = df_agri_daily['time'].dt.day_name()

    return df_agri, df_agri_daily


def merge_daily_data(df_std, df_agri_daily):

    merged_df = pd.merge(df_std, df_agri_daily, left_on='datetime', right_on='time', how='left')
    merged_df = merged_df.iloc[1:]
    merged_df['precip'] = merged_df['precip'].fillna(0)

    return merged_df


def export_datasets(merged_df, df_agri):
    merged_df.to_csv(r'C:\Users\felix\OneDrive\Dokumente\Python Projects\End-to-End-Project_AgriAnalytics\merged_df.csv', index=False)
    df_agri.to_csv(r'C:\Users\felix\OneDrive\Dokumente\Python Projects\End-to-End-Project_AgriAnalytics\df_agri.csv', index=False)


# -----------------
# Define DAG object
# -----------------



with DAG("agri_tech", start_date=datetime(2025,7,21),
         schedule_interval="@weekly",
         catchup=False) as dag:
    
    loading_std_data = PythonOperator(
        task_id = "load_std_data",
        python_callable = std_data_extract)

    
    loading_agri_data = PythonOperator(
        task_id = "load_agri_data",
        python_callable = agri_data_extract)

    
    prep_std_dataset = PythonOperator(
        task_id = "prep_data_std",
        python_callable = prep_std_data)
    
    prep_agri_dataset = PythonOperator(
        task_id = "prep_data_agri",
        python_callable = prep_agri_data)
    
    combine_daily = PythonOperator(
        task_id = "combine_daily_data",
        python_callable = merge_daily_data)

    export_data = PythonOperator(
        task_id = "export_csv",
        python_callable = export_datasets)
    

    loading_std_data >> prep_std_dataset
    loading_agri_data >> prep_agri_dataset
    [prep_std_dataset, prep_agri_dataset] >> combine_daily
    combine_daily >> export_data


        