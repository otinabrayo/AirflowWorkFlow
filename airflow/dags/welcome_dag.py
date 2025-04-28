from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore[import]
from datetime import timedelta, datetime


def welcome_message():
    print("Welcome to Airflow Learning")

def todays_date():
    print('Today is {}'.format(datetime.today().date()))

def random_mess():
    name = "Joseph"
    print(f"My father is a gangster called {name}")

default_args = {
    "start_date" : datetime.now() - timedelta(days=1)
}

dag = DAG(
    'welcome_dag',
    default_args=default_args,
    schedule='0 23 * * *',
    catchup=False
)

welcome_task = PythonOperator(
    task_id='Welcome_messege',
    python_callable=welcome_message,
    dag=dag
)

todays_date_task = PythonOperator(
    task_id="Todays_date",
    python_callable=todays_date,
    dag=dag
)

random_messege_task = PythonOperator(
    task_id='Random_messege',
    python_callable=random_mess,
    dag=dag
)

welcome_task >> todays_date_task >> random_messege_task