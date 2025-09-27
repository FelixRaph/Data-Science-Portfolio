from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import task_group
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.state import State
from airflow.models import DagRun
from airflow.exceptions import AirflowSkipException
from sqlalchemy import create_engine
from airflow.hooks.base import BaseHook
import pandas as pd
from datetime import datetime, timedelta

# import merge_daily_data, export_datasets functions here


def prep_std_data(**kwargs):
    ti = kwargs['ti']
    # df_std = pd.read_json(ti.xcom_pull(task_ids='load_data.load_std_data'))
    df_std = pd.read_json('/tmp/std_prep.json')
    df_std['datetime'] = pd.to_datetime(df_std['datetime'])
    df_std['day_name'] = df_std['datetime'].dt.day_name()
    columns_to_drop = ['severerisk', 'datetimeEpoch', 'sunriseEpoch', 'sunsetEpoch']
    df_std.drop(columns=[col for col in columns_to_drop if col in df_std.columns], inplace=True)

    return df_std.to_json()


def prep_agri_data(**kwargs):
    ti = kwargs['ti']
    df_agri = pd.read_json('/tmp/agri_prep.json')
    df_agri['time'] = pd.to_datetime(df_agri['time'])
    df_agri['time'] = df_agri['time'].dt.tz_localize(None)

    numeric_cols = df_agri.select_dtypes(include='number').columns
    df_agri_daily = df_agri.groupby(pd.Grouper(key='time', freq='D'))[numeric_cols].mean().round(3).reset_index()
    df_agri_daily['day_name'] = df_agri_daily['time'].dt.day_name()

    return df_agri_daily.to_json()




def merge_daily_data(**kwargs):
    ti = kwargs['ti']
    df_std = pd.read_json(ti.xcom_pull(task_ids='prep_data_std'), convert_dates=['datetime'])
    df_agri_daily = pd.read_json(ti.xcom_pull(task_ids='prep_data_agri'), convert_dates=['time'])

    df_std['datetime'] = pd.to_datetime(df_std['datetime'])
    df_agri_daily['time'] = pd.to_datetime(df_agri_daily['time'])


    print(df_std.dtypes)
    print(df_agri_daily.dtypes)

    # Rename for merging
    df_std.rename(columns={"datetime": "time"}, inplace=True)

    # Try merge
    merged_df = pd.merge(df_agri_daily, df_std, on='time', how='inner')

    # Post-process
    merged_df = merged_df.iloc[1:]
    merged_df['precip'] = merged_df.get('precip', 0)
    merged_df.columns = merged_df.columns.str.replace('[.]', '_', regex=True)
    merged_df.columns = merged_df.columns.str.lower()

    return merged_df.to_json()






# ----------------------
# Export to a database
# ----------------------



def export_datasets(**kwargs):
    ti = kwargs['ti']
    
    merged_data_json = ti.xcom_pull(task_ids='combine_daily_data')
    merged_df = pd.read_json(merged_data_json)
    merged_df['time'] = pd.to_datetime(merged_df['time'], errors='coerce')

        
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



def wait_for_latest_dag1(**kwargs):
    dag_runs = DagRun.find(dag_id='agri_tech_data_load_prep', state=State.SUCCESS)
    if not dag_runs:
        raise AirflowSkipException("No successful run of DAG 1 found yet.")
    print(f"Latest DAG 1 run: {dag_runs[-1].execution_date}")
    return True



with DAG("agri_tech_data_merge_export",
         start_date=datetime(2025, 7, 23),
         schedule_interval='0 6 * * *',
         catchup=False) as dag:

    wait_for_load_prep = PythonOperator(
        task_id="wait_for_load_prep",
        python_callable=wait_for_latest_dag1,
)

    merge_data = PythonOperator(
        task_id="combine_daily_data",
        python_callable=merge_daily_data,
        provide_context=True
    )

    export_data = PythonOperator(
        task_id="export_data",
        python_callable=export_datasets,
        provide_context=True
    )

    prep_std = PythonOperator(
        task_id="prep_data_std",
        python_callable=prep_std_data,
        provide_context=True
)

    prep_agri = PythonOperator(
        task_id="prep_data_agri",
        python_callable=prep_agri_data,
        provide_context=True
)


wait_for_load_prep >> [prep_std, prep_agri] >> merge_data >> export_data
