from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from airflow.providers.snowflake.operators.snowflake import SnowflakeCheckOperator


# Combination of traditional dec and taskflow dec

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
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 21 * * *',
    catchup=False
)

with dag:
    load_task = load(validate(transform(extract())))

    snowflake_task = SnowflakeCheckOperator(
        task_id='Snowflake_task',
        sql='select 1',
        snowflake_conn_id='snowflake_conn_id',
    )

    load_task >> snowflake_task
