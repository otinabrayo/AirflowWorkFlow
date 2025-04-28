from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from airflow.providers.standard.operators.bash import BashOperator # type: ignore
from datetime import timedelta, datetime
from clean_data import clean_data
from email_trigger import EmailTrigger


def task_failure_alert(context):
    print(f"Task has failed, task_instance_key_str: {context['task_instance_key_str']}")

def success_email(context):
    EmailTrigger(
        subject="Exchange Rate DAG success🎯",
        body="The DAG has successfully fetched cleaned and loaded 🔥🔥🔥."
    )

default_args = {
    "retries": 2,
    "retry_delay": timedelta(days=2),
    "start_date":datetime(2025, 4, 27),
    "end_date":datetime(2025, 12, 31),
}

# Defining and Initiating DAG
dag = DAG(
    'exchange_rate_etl',
    schedule='0 23 * * *',
    default_args=default_args,
    catchup=False,
    on_success_callback=success_email,
    on_failure_callback=task_failure_alert
)

# Defining and Initiating Tasks
download_task = BashOperator(
    task_id='download_file',
    bash_command='curl -o xrate.csv https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata ',
    cwd='/tmp',
    dag=dag
)

clean_data_task = PythonOperator(
    task_id='data_cleaning',
    python_callable=clean_data,
    dag=dag
)

# Define task dependancies
download_task >> clean_data_task