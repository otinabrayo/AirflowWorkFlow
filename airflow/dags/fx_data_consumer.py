from airflow import DAG, Dataset
from airflow.providers.snowflake.operators.snowflake import SnowflakeCheckOperator
from datetime import datetime, timedelta
from email_trigger import EmailTrigger


default_args={
    "start_date":datetime.now() - timedelta(days=1)
}

def send_mail(context):
    EmailTrigger(
        subject="❄Snowflake Alert ⚠",
        body='Data Has been loaded successfully ✔✔ and ready for analysis'
    )

dag = DAG(
    'data_consumer_dag',
    default_args=default_args,
    schedule=[Dataset("s3://reddit-airflow-bucket-otina/oms/xrate_.json")],
    on_success_callback=send_mail

    # usually cron based
)

load_table= SnowflakeCheckOperator(
    task_id='data_consumer_task',
    sql='./sqls/xrate_sf.sql',
    snowflake_conn_id='snowflake_conn_id',
    dag=dag
)

load_table