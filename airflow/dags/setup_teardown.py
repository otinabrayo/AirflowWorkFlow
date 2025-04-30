from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


dag = DAG(
    'setup_teardown',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 23 * * *',
    catchup=False
)

# Define tasks
create_cluster = PythonOperator(
    task_id='create_cluster',
    python_callable=lambda: print("Creating Cluster"),
    dag=dag,
)

run_query1 = PythonOperator(
    task_id='run_query1',
    python_callable=lambda: print("Running Query 1"),
    dag=dag,
)

run_query2 = PythonOperator(
    task_id='run_query2',
    python_callable=lambda: print("Running Query 2"),
    dag=dag,
)

# run_query2 = PythonOperator(
#     task_id='run_query2',
#     python_callable=lambda: raise_exception("Failure in Query 2"),
#     dag=dag,
# )

run_query3 = PythonOperator(
    task_id='run_query3',
    python_callable=lambda: print("Running Query 3"),
    dag=dag,
)

delete_cluster = PythonOperator(
    task_id='delete_cluster',
    python_callable=lambda: print("Deleting Cluster"),
    dag=dag,
)

# Define task dependencies
create_cluster >> [run_query1, run_query2]
[run_query1, run_query2] >> run_query3
run_query3 >> delete_cluster.as_teardown(setups=create_cluster)