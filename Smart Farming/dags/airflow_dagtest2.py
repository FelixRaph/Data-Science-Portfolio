# ---------------------------------------------------------
# Airflow Code
# ---------------------------------------------------------

'''
In this script, we extract, process, and export weather and agricultural data.
'''

# -----------------
# Load libraries
# -----------------

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

    return df_std.to_json()


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

    return df_agri.to_json()


# -----------------
# Data Cleaning & Transformation
# -----------------

def prep_std_data(**kwargs):
    ti = kwargs['ti']
    df_std = pd.read_json(ti.xcom_pull(task_ids='load_data.load_std_data'))
    df_std['datetime'] = pd.to_datetime(df_std['datetime'])
    df_std['day_name'] = df_std['datetime'].dt.day_name()
    columns_to_drop = ['severerisk', 'datetimeEpoch', 'sunriseEpoch', 'sunsetEpoch']
    df_std.drop(columns=[col for col in columns_to_drop if col in df_std.columns], inplace=True)

    return df_std.to_json()


def prep_agri_data(**kwargs):
    ti = kwargs['ti']
    df_agri = pd.read_json(ti.xcom_pull(task_ids='load_data.load_agri_data'))

    # Convert milliseconds to seconds before datetime conversion
    df_agri['time'] = pd.to_datetime(df_agri['time'] / 1000, unit='s').dt.tz_localize(None)

    numeric_cols = df_agri.select_dtypes(include='number').columns
    df_agri_daily = df_agri.groupby(pd.Grouper(key='time', freq='D'))[numeric_cols].mean().round(3).reset_index()
    df_agri_daily['day_name'] = df_agri_daily['time'].dt.day_name()

    return df_agri_daily.to_json()



def merge_daily_data(**kwargs):
    ti = kwargs['ti']
    df_std = pd.read_json(ti.xcom_pull(task_ids='prep_data.prep_data_std'))
    df_agri_daily = pd.read_json(ti.xcom_pull(task_ids='prep_data.prep_data_agri'))

    # Normalize and force remove any microseconds/timezone
    df_std['datetime'] = pd.to_datetime(df_std['datetime']).dt.normalize().dt.floor('D')
    df_agri_daily['time'] = pd.to_datetime(df_agri_daily['time']).dt.normalize().dt.floor('D')


    # Print for debugging
    print("=== STD TIMES ===")
    print(df_std['datetime'].unique())
    print("=== AGRI TIMES ===")
    print(df_agri_daily['time'].unique())

    # Rename for merging
    df_std.rename(columns={"datetime": "time"}, inplace=True)

    # Try merge
    merged_df = pd.merge(df_agri_daily, df_std, on="time", how="inner")

    # Post-process
    merged_df = merged_df.iloc[1:]
    merged_df['precip'] = merged_df.get('precip', 0)
    merged_df.columns = merged_df.columns.str.replace('[.]', '_', regex=True)
    merged_df.columns = merged_df.columns.str.lower()

    print("=== MERGED ROWS ===")
    print(len(merged_df))

    return merged_df.to_json()




# ----------------------
# Export to a database
# ----------------------



def export_datasets(**kwargs):
    ti = kwargs['ti']
    
    merged_data_json = ti.xcom_pull(task_ids='prep_data.combine_daily_data')
    merged_df = pd.read_json(merged_data_json)
        
    postgres_hook = PostgresHook(postgres_conn_id='agri_project_connection', schema='agriculture_tech')
    
    table_name = 'agri_weather_data'    
    
    engine = create_engine(
    f"postgresql+psycopg2://{'airflow'}:{'felixdoesdatascience'}@{'materials-postgres-1'}:{5432}/{'airflow'}"
)

    try:
        merged_df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False,
            method='multi'
        )
        
        print(f"Successfully inserted {len(merged_df)} rows into {table_name}")
    
        
    except Exception as e:
        print(f"Error inserting data: {e}")
        raise

    



# -----------------
# Define DAG object
# -----------------

with DAG("agri_tech_api_data_pipeline",
         start_date=datetime(2025, 7, 23, 6, 0, 0),
         schedule_interval='0 6 * * *',
         catchup=False) as dag:
    
    @task_group(group_id="load_data")
    def load_group():
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
            """,
            autocommit=True,
        )


        loading_std_data = PythonOperator(
            task_id="load_std_data",
            python_callable=std_data_extract,
            provide_context=True,
            do_xcom_push=True
        )

        loading_agri_data = PythonOperator(
            task_id="load_agri_data",
            python_callable=agri_data_extract,
            provide_context=True,
            do_xcom_push=True
        )

        create_table >> [loading_std_data, loading_agri_data]


    @task_group(group_id="prep_data")
    def prep_group():

        prep_std_dataset = PythonOperator(
            task_id="prep_data_std",
            python_callable=prep_std_data,
            provide_context=True
        )

        prep_agri_dataset = PythonOperator(
            task_id="prep_data_agri",
            python_callable=prep_agri_data,
            provide_context=True
        )

        combine_daily = PythonOperator(
            task_id="combine_daily_data",
            python_callable=merge_daily_data,
            provide_context=True
        )

        export_data = PythonOperator(
            task_id="export_data",
            python_callable=export_datasets,
            provide_context=True
        )

        [prep_std_dataset, prep_agri_dataset] >> combine_daily >> export_data

    load = load_group()
    prep = prep_group()

    load >> prep