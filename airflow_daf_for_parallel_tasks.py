from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 5, 0, 0),
    'catchup': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'first_dag_for_parallel_tasks',
    default_args=default_args,
    description='A simple for parallel tasks',
    schedule_interval='*/2 * * * *',  # Every two minutes
)

start_task = BashOperator(
    task_id='start_task',
    bash_command='echo "Starting the DAG!"',
    dag=dag,
)
parallel_task_1 = BashOperator(
    task_id='parallel_task_1',
    bash_command='echo "Running parallel task 1!"',
    dag=dag,
)
parallel_task_2 = BashOperator(
    task_id='parallel_task_2',
    bash_command='echo "Running parallel task 2!"',
    dag=dag,
)
parallel_task_3 = BashOperator(
    task_id='parallel_task_3',
    bash_command='echo "Running parallel task 3!"',
    dag=dag,
)

end_task = BashOperator(
    task_id='end_task',
    bash_command='echo "Ending the DAG!"',
    dag=dag,
)   

start_task >> [parallel_task_1, parallel_task_2, parallel_task_3] >> end_task
# This DAG has a start task, three parallel tasks, and an end task.