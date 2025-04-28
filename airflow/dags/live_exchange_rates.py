from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from airflow.providers.standard.operators.bash import BashOperator # type: ignore
from datetime import timedelta, datetime
from email_trigger import EmailTrigger


def success_mail(context):
    EmailTrigger(
        subject=" Live Currency Rate DAG success🎯",
        body="The Live currency exchange rate DAG has been successfully fetched and loaded🔥🔥🔥."
    )

default_args = {
    "retries": 2,
    "retry_delay": timedelta(days=2),
    "start_date":datetime(2025, 4, 27),
    "end_date":datetime(2025, 12, 31),
}

# Defining and Initiating DAG
dag = DAG(
    'live_exchange_rates',
    schedule='0 23 * * *',
    default_args=default_args,
    catchup=False,
    on_success_callback=success_mail,
)

# Defining and Initiating Tasks
fetch_exchange_rates = BashOperator(
    task_id='download_file',
    bash_command="curl '{{ var.value.get(\"web_api_key\") }}' ",
    cwd='/tmp',
    dag=dag
)

# Define task dependancies
fetch_exchange_rates