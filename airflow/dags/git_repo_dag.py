from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.github.operators.github import GithubOperator
from airflow.operators.empty import EmptyOperator
import logging

def task_failure_alert(context):
    print(f"Task has failed, task_instance_key_str: {context['task_instance_key_str']}")


default_args = {
    "start_date" : datetime.now() - timedelta(days=1)
}

# Define the DAG
dag = DAG(
    'git_repo_dag',
    default_args=default_args,
    schedule='0 21 * * *',
    catchup=False,
    on_failure_callback=task_failure_alert
)

# Start Dummy Operator
start = EmptyOperator(task_id='start', dag=dag)

# List GitRepository Tags
list_repo_tags = GithubOperator(
    task_id="list_repo_tags",
    github_conn_id="github_default",
    github_method="get_repo",
    github_method_args={"full_name_or_id": "otinabrayo/ApacheAirflow"},
    result_processor=lambda repo: logging.info(list(repo.get_tags())),
    dag=dag,
)

# End Dummy Operator
end = EmptyOperator(task_id='end', dag=dag)

# Define task dependencies
start >> list_repo_tags >> end