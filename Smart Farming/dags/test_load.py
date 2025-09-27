from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import task_group
from sqlalchemy import create_engine
from airflow.hooks.base import BaseHook
import requests
import sys
import pandas as pd
from datetime import datetime, timedelta

# import your functions std_data_extract, agri_data_extract, prep_std_data, prep_agri_data here

# -----------------
# API data load
# -----------------

# --------------------------------------------------------
# Extract standard weather data: using VisualCrossing
# --------------------------------------------------------

def std_data_extract(**kwargs):
    response_standard_data = requests.get(
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Rotterdam/last7days?unitGroup=metric&include=obs&key=XTJF7TPU48LF8YN9TXGMG7C8N&contentType=json&include=days"        
    )
    if response_standard_data.status_code != 200:
        print('Unexpected Status code: ', response_standard_data.status_code)
        sys.exit()

    data = response_standard_data.json()
    df_std = pd.json_normalize(data['days'])
    df_std['location'] = data['resolvedAddress']
    df_std['latitude'] = data['latitude']
    df_std['longitude'] = data['longitude']

    if 'hours' in df_std.columns:
        df_std = df_std.drop('hours', axis=1)

    return df_std.to_json('/tmp/std_prep.json')


# --------------------------------------------------------
# Extract agricultural data: using stormglass.io
# --------------------------------------------------------

def agri_data_extract(**kwargs):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    response = requests.get(
        'https://api.stormglass.io/v2/bio/point',
        params={
            'lat': 51.9144,
            'lng': 4.48717,
            'params': ','.join([
                'soilMoisture', 'soilMoisture10cm', 'soilMoisture40cm',
                'soilTemperature', 'soilTemperature10cm', 'soilTemperature40cm'
            ]),
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

    return df_agri.to_json('/tmp/agri_prep.json')




with DAG("agri_tech_data_load_prep",
         start_date=datetime(2025, 7, 23),
         schedule_interval='0 6 * * *',
         catchup=False) as dag:

    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_agri_tech",
        database="airflow",
        sql="""
            CREATE TABLE IF NOT EXISTS agri_weather_data (
                id SERIAL PRIMARY KEY,
                time TIMESTAMP,
                tempmax FLOAT,
                tempmin FLOAT,
                temp FLOAT,
                feelslikemax FLOAT,
                feelslikemin FLOAT,
                feelslike FLOAT,
                dew FLOAT,
                humidity FLOAT,
                precip FLOAT,
                precipprob FLOAT,
                precipcover FLOAT,
                preciptype VARCHAR(50),
                snow FLOAT,
                snowdepth FLOAT,
                windgust FLOAT,
                windspeed FLOAT,
                winddir FLOAT,
                pressure FLOAT,
                cloudcover FLOAT,
                visibility FLOAT,
                solarradiation FLOAT,
                solarenergy FLOAT,
                uvindex FLOAT,
                sunrise VARCHAR(20),
                sunset VARCHAR(20),
                moonphase FLOAT,
                conditions VARCHAR(100),
                description TEXT,
                icon VARCHAR(50),
                stations TEXT,
                source VARCHAR(50),
                location VARCHAR(200),
                latitude FLOAT,
                longitude FLOAT,
                day_name_x VARCHAR(20),
                soilmoisture_ecmwf FLOAT,
                soilmoisture_noaa FLOAT,
                soilmoisture_sg FLOAT,
                soilmoisture10cm_ecmwf FLOAT,
                soilmoisture10cm_noaa FLOAT,
                soilmoisture10cm_sg FLOAT,
                soilmoisture40cm_ecmwf FLOAT,
                soilmoisture40cm_noaa FLOAT,
                soilmoisture40cm_sg FLOAT,
                soiltemperature_ecmwf FLOAT,
                soiltemperature_noaa FLOAT,
                soiltemperature_sg FLOAT,
                soiltemperature10cm_ecmwf FLOAT,
                soiltemperature10cm_noaa FLOAT,
                soiltemperature10cm_sg FLOAT,
                soiltemperature40cm_ecmwf FLOAT,
                soiltemperature40cm_noaa FLOAT,
                soiltemperature40cm_sg FLOAT,
                day_name_y VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ,  # your create table sql here
        autocommit=True,
    )

    load_std_data = PythonOperator(
        task_id="load_std_data",
        python_callable=std_data_extract,
        provide_context=True,
        do_xcom_push=True
    )

    load_agri_data = PythonOperator(
        task_id="load_agri_data",
        python_callable=agri_data_extract,
        provide_context=True,
        do_xcom_push=True
    )


    create_table >> [load_std_data, load_agri_data]
