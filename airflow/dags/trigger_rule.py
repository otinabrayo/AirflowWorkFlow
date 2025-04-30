from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


dag = DAG(
    'triger_rules',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 23 * * *',
    catchup=False
)

# Define tasks
task_a = PythonOperator(
    task_id='task_a',
    python_callable=lambda: raise_exception("Failure in Query a"),
    dag=dag,
)

task_b = PythonOperator(
    task_id='task_b',
    python_callable=lambda: raise_exception("Failure in Query b"),
    dag=dag,
)

task_c = PythonOperator(
    task_id='task_c',
    python_callable=lambda: raise_exception("Failure in Query c"),
    dag=dag,
)

task_d = PythonOperator(
    task_id='task_d',
    python_callable=lambda: print("Executing Task D"),
    dag=dag,
    trigger_rule='all_failed',
)

task_e = PythonOperator(
    task_id='task_e',
    python_callable=lambda: print("Executing Task E"),
    dag=dag,
)

# Define task dependencies
task_a >> task_d
task_b >> task_d
task_c >> task_d
task_d >> task_e
