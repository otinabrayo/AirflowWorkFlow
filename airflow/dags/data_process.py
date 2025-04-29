from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor # type: ignore
from airflow.providers.snowflake.transfers.copy_into_snowflake import CopyFromExternalStageToSnowflakeOperator# type: ignore
from datetime import timedelta, datetime
from email_trigger import EmailTrigger


def send_mail(context):
    EmailTrigger(
        subject="S3 to ❄flake",
        body="S3 files have been succesfully triggered by the sensor and loaded to snowflake for further analyzation"
    )

default_args = {
    'start_date': datetime.now() - timedelta(days=1)
}

dag = DAG(
    's3_to_snowflake_dag',
    default_args=default_args,
    schedule='0 23 * * *',
    catchup=False,
    on_success_callback=send_mail
)

# Waiting for the file in s3
file_waiting = S3KeySensor(
    task_id='wait_for_s3_file',
    bucket_name='reddit-airflow-bucket-otina',
    bucket_key='medals.csv',
    aws_conn_id='aws-default',
    poke_interval=60 * 10,
    mode='reschedule',
    timeout=60 * 60 * 5,
    soft_fail=True,
    deferrable=True,
    dag=dag
)

# Load the file from s3 to snowflake
load_table = CopyFromExternalStageToSnowflakeOperator(
    task_id='load_s3_file_to_table',
    snowflake_conn_id='snowflake_conn_id',
    files=['medals.csv'],
    table='MEDALS',
    stage='my_s3_stage',
    file_format="(TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1 ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE FIELD_OPTIONALLY_ENCLOSED_BY = '\"')",
    dag=dag
)

file_waiting >> load_table
