import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Test email from Airflow")
msg['Subject'] = "Test Email"
msg['From'] = "otibra00@gmail.com"
msg['To'] = "marionkoki00@gmail.com"

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("otibra00@gmail.com", "qqullnfzzkhukfwd")
        server.sendmail("otibra00@gmail.com", "marionkoki00@gmail.com", msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")




    Task Flow API:
from airflow import DAG

from airflow.decorators import task
from airflow.utils.dates import days_ago

@task
def extract():
    # Extract logic here
    return "Raw order data"
@task
def transform(raw_data):
    # Transform logic here
    return f"Processed: {raw_data}"
@task
def validate(processed_data):
    # Validate logic here
    return f"Validated: {processed_data}"
@task
def load(validated_data):
    # Load logic here
    print(f"Data loaded successfully: {validated_data}")

dag = DAG(
    'taskflow_api',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 21 * * *',
    catchup=False
)

with dag:
    load_task = load(validate(transform(extract())))




2) Traditional:

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def extract(ti=None, **kwargs):
    # Extract logic here
    raw_data = "Raw order data"
    ti.xcom_push(key="raw_data", value=raw_data)

def transform(ti=None, **kwargs):
    # Transformation logic here
    raw_data = ti.xcom_pull(task_ids="extract", key="raw_data")
    processed_data = f"Processed: {raw_data}"
    ti.xcom_push(key="processed_data", value=processed_data)

def validate(ti=None, **kwargs):
    # Validation logic here
    processed_data = ti.xcom_pull(task_ids="transform", key="processed_data")
    validated_data = f"Validated: {processed_data}"
    ti.xcom_push(key="validated_data", value=validated_data)

def load(ti=None, **kwargs):
    # Load logic here
    validated_data = ti.xcom_pull(task_ids="validate", key="validated_data")
    print(f"Data loaded successfully: {validated_data}")

dag = DAG(
    'traditional_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 21 * * *',
    catchup=False
)

extract_task = PythonOperator(
    task_id="extract",
    python_callable=extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform",
    python_callable=transform,
    dag=dag,
)

validate_task = PythonOperator(
    task_id="validate",
    python_callable=validate,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load",
    python_callable=load,
    dag=dag,
)

# Set Dependencies
extract_task >> transform_task >> validate_task >> load_task




3) Hybrid:

from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

@task
def extract():
    # Extract logic here
    return "Raw order data"

@task
def transform(raw_data):
    # Transform logic here
    return f"Processed: {raw_data}"

@task
def validate(processed_data):
    # Validate logic here
    return f"Validated: {processed_data}"

@task
def load(validated_data):
    # Load logic here
    print(f"Data loaded successfully: {validated_data}")

dag = DAG(
    'hybrid_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 21 * * *',
    catchup=False
)

with dag:
    load_task = load(validate(transform(extract())))

    snowflake_task = SnowflakeOperator(
        task_id='Snowflake_task',
        sql='select 1',
        snowflake_conn_id='snowflake_conn',
    )

    load_task >> snowflake_task
