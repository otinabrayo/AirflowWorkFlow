from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from airflow.providers.amazon.aws.hooks.s3 import S3Hook # type: ignore
from datetime import timedelta, datetime
from email_trigger import EmailTrigger

default_args = {
    'start_date': datetime.now() - timedelta(days=1)
}

def send_mail(context):
    EmailTrigger(
        subject=" YAAAAY ✨✨🧨File Transformation",
        body="Your filea have been successfully transformed HURAY"
    )

def custom_transformation(bucketname, sourcekey, destinationkey):
    s3_hook = S3Hook(aws_conn_id='aws-default')

    # read s3 file
    content = s3_hook.read_key(bucket_name=bucketname, key=sourcekey)

    # apply custom transformation
    transformed_content = content.upper()

    # load s3 file
    s3_hook.load_string(
        transformed_content,
        bucket_name=bucketname,
        key=destinationkey
    )

dag = DAG(
    'custom_s3_transformation',
    default_args=default_args,
    schedule='0 23 * * *',
    catchup=False,
    on_success_callback=send_mail
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=custom_transformation,
    op_args=['reddit-airflow-bucket-otina', 'oms/reddit_posts.csv', 'transformed_reddit_posts.csv'],
    dag=dag
)

transform_task