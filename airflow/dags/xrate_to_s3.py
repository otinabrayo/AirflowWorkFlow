from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator # type: ignore
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator# type: ignore
from datetime import timedelta, datetime
from email_trigger import EmailTrigger
import subprocess


default_args = {
    'start_date': datetime.now() - timedelta(days=1)
}
def send_mail(context):
    EmailTrigger(
        subject="Files📁 to s3_🗑",
        body="Your 📂files have been succesfully fetched and 🗃loaded to S3 bucket for further analyzation"
    )

def fetch_xrate(ti, **kwargs):
    xrate_filename= f'xrate_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.json'
    curl_command = ["curl", Variable.get('web_api_key'), "-o" f'/tmp/{xrate_filename}']
    subprocess.run(curl_command, check=True)
    ti.xcom_push(key='xrate_file', value=xrate_filename)

dag = DAG(
    'Exchange_rate_to_s3',
    default_args=default_args,
    schedule='0 23 * * *',
    catchup=False,
    on_success_callback=send_mail
)

# Difine tasks
fetch_lxrate = PythonOperator(
    task_id="fetch_xrate",
    python_callable=fetch_xrate,
    dag=dag
)

upload_to_s3 = LocalFilesystemToS3Operator(
    task_id='upload_to_s3',
    filename="/tmp/{{ ti.xcom_pull(task_ids='fetch_xrate', key='xrate_file') }}",
    dest_bucket='reddit-airflow-bucket-otina',
    dest_key=f"{{{{ ti.xcom_pull(task_ids='fetch_xrate', key='xrate_file') }}}}",
    aws_conn_id='aws-default',
    replace=True,
    dag=dag
)

fetch_lxrate >> upload_to_s3

