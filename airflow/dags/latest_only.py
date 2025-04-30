from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.latest_only import LatestOnlyOperator
from datetime import datetime, timedelta
from email_trigger import EmailTrigger


# Send email based on success
def send_email_completed(context):
    EmailTrigger(
        subject="UK Sales Data Load - Successful",
        body="UK Sales Data Load Completed Successfully.",
    )

# Send email based on failure
def send_email_failed(context):
    EmailTrigger(
        subject="UK Sales Data Load  - Failed",
        body="UK Sales Data Load Failed. Please check the logs for more details.",
    )


dag = DAG(
    'LatestOnly',
    default_args={'start_date': datetime.now() - timedelta(days=8)},
    schedule='0 2 * * *',
    catchup=True,
    on_success_callback=send_email_completed,
    on_failure_callback=send_email_failed
)

# Define tasks
task_a = PythonOperator(
    task_id='task_a',
    python_callable=lambda: print("Executing Task A"),
    dag=dag,
)

task_b = PythonOperator(
    task_id='task_b',
    python_callable=lambda: print("Executing Task B"),
    depends_on_past=True,
    dag=dag,
)

# task_b = PythonOperator(
#     task_id='task_b',
#     python_callable=lambda: raise_exception("Executing Task B Failed"),
#     dag=dag,
# )

# Task for LatestOnlyOperator branch
latest_only = LatestOnlyOperator(
    task_id="latest_only",
    dag=dag
)

# Connect tasks
task_a >> task_b
task_b >> latest_only
