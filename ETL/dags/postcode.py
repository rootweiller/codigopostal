from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from ETL.integration.integration import IntegrationPostCode

default_args = {
    'owner': 'Rootweiller',
    'depends_on_past': False,
    'start_date':  datetime(2020, 4, 18),
    'email': ['juan@rootweiller.xyz'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1
}


data_type = 'search'

dag = DAG(
    'PostCode__{0}'.format(data_type),
    description='Post Codes Search ',
    default_args=default_args,
    schedule_interval='@daily'
)

pending_files = IntegrationPostCode()

extract_data_csv = PythonOperator(
    task_id='{0}'.format(data_type),
    python_callable=pending_files.execute,
    op_args=[data_type],
    dag=dag
)


get_info_postcode = PythonOperator(
    task_id='{0}'.format(data_type),
    python_callable=pending_files.get_postcode_api,
    op_args=[data_type],
    dag=dag
)

extract_data_csv >> get_info_postcode

