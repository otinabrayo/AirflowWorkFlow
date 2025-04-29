from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeCheckOperator  # type: ignore
from datetime import datetime, timedelta
from email_trigger import EmailTrigger

default_args = {
    'start_date': datetime.now() - timedelta(days=1)
}

def success_mail(context):
    EmailTrigger(
        subject="UK profit table successfull❄",
        body="UK Sales table to Profit table Load completed"
    )

dag = DAG(
    'load_profit_uk',
    default_args=default_args,
    schedule='0 23 * * *',
    catchup=False,
    on_success_callback=success_mail
)

load_table = SnowflakeCheckOperator(
    task_id='load_table',
    sql='./sqls/profit_uk.sql',
    snowflake_conn_id='snowflake_conn_id',
    dag=dag
)

load_table