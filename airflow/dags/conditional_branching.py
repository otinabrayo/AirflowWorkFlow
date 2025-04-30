from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator


# Getting file size
def get_file_size(file_path, ti):
    # get_file size in bytes
    with open(file_path, 'rb') as f:
        file_size_bytes = len(f.read())

    # convert bytes to gb
    file_size_gb = file_size_bytes / (1024 ** 3)

    # push file size to Xcom
    ti.xcom_push(key='file_size', value=file_size_bytes)

# Deciding the branch
def decide_branch(ti):
    file_size = ti.xcom_pull(task_ids='check_file_size', key='file_size')
    return 'parallel_transform' if file_size > 10 else 'serial_transform'

# Serial transformation task
def serial_transform():
    # Transformation logic
    print('Executing serial transformation')

# Serial load task
def serial_load():
    # Serial load logic
    print("Executing serial load")

# Parallel transformation task
def parallel_transform():
    # Parallel transformation logic
    print("Executing parallel transformation")

# Parallel load task
def parallel_load():
    # Parallel load logic
    print("Executing parallel load")


dag = DAG(
    'conditional_branching',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 23 * * *',
    catchup=False
)

# Task to check file size
check_file_size = PythonOperator(
    task_id='check_file_size',
    python_callable=get_file_size,
    op_args=['/tmp/dats/uk.dat'],
    dag=dag
)

# Task to decide the branch
decide_branch_task = BranchPythonOperator(
    task_id='decide_branch',
    python_callable=decide_branch,
    dag=dag
)

# Define tasks for serial execution
serial_transform_task = PythonOperator(
    task_id='serial_transform',
    python_callable=serial_transform,
    dag=dag
)

serial_load_task = PythonOperator(
    task_id='serial_load',
    python_callable=serial_load,
    dag=dag
)

# Define tasks for parallel execution
parallel_transform_task = PythonOperator(
    task_id='parallel_transform',
    python_callable=parallel_transform,
    dag=dag
)

parallel_load_task = PythonOperator(
    task_id='parallel_load',
    python_callable=parallel_load,
    dag=dag
)

# Set up task dependencies
check_file_size >> decide_branch_task

# Serial branch
decide_branch_task >> serial_transform_task >> serial_load_task

# Parallel branch
decide_branch_task >> parallel_transform_task >> parallel_load_task