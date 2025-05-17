from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

def hello_world(*args, **kwargs):
    print("Hello, World from PythonOperator!")

default_args = {
'start_date': datetime(2025, 4, 5, 0, 0)
}


dag=DAG(
    'first_dag',
    default_args=default_args,
    description='A simple first DAG',
    #schedule_interval=None,
    schedule_interval='*/1 * * * *', # Every minute
)

t1=BashOperator(
    task_id='print_hello_from_linux_command',
    bash_command='echo "Hello from BashOperator!"',
    dag=dag,    
)

t2=PythonOperator(
    task_id='print_hello_from_python_command',
    python_callable=hello_world,
    dag=dag,
)

t1 >> t2
# This DAG has two tasks: t1 and t2.
