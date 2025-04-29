from airflow import DAG, Dataset
from airflow.providers.amazon.aws.transfers.http_to_s3 import HttpToS3Operator
from airflow.models import Variable
from datetime import datetime, timedelta

default_args={
    "start_date":datetime.now() - timedelta(days=1)
}

dag = DAG(
    'data_producer_dag',
    default_args=default_args,
    schedule='0 23 * * *',
)

http_to_s3 = HttpToS3Operator(
    task_id='data_producer_task',
    # endpoint=Variable.get('web_api_key'),
    s3_bucket='reddit-airflow-bucket-otina',
    s3_key='oms/xrate_.json',
    aws_conn_id='aws-default',
    http_conn_id='http_conn_id_default',
    endpoint='/v6/794264d0e7292bbab883281b/latest/USD',
    replace=True,
    dag=dag,
    outlets=[Dataset("s3://reddit-airflow-bucket-otina/oms/xrate_.json")],
)
