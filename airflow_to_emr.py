# Import necessary modules from Airflow and Python standard library
from airflow import DAG  # DAG is used to define the workflow structure
from airflow.providers.amazon.aws.operators.emr import EmrAddStepsOperator  # Operator to add steps to an EMR cluster
from airflow.providers.amazon.aws.sensors.emr import EmrStepSensor  # Sensor to monitor the status of an EMR step
from datetime import datetime  # Used to define the start date of the DAG

# Define the DAG (Directed Acyclic Graph) for the workflow
dag = DAG(
    'submit_pyspark_job_to_emr',  # Unique identifier for the DAG
    start_date=datetime(2021, 1, 1),  # The date from which the DAG will start running
    catchup=False,  # If False, Airflow will not backfill missed runs
    tags=['test'],  # Tags help categorize and filter DAGs in the Airflow UI
)

# Define the task to add a step to the EMR cluster
step_adder = EmrAddStepsOperator(
    task_id='add_step',  # Unique identifier for this task
    job_flow_id='j-27VNZHQ1YT7OW',  # The ID of the EMR cluster where the step will be added
    aws_conn_id='aws_default',  # Connection ID for AWS credentials configured in Airflow
    steps=[{  # List of steps to be added to the EMR cluster
        'Name': 'Run PySpark Script',  # Name of the step
        'ActionOnFailure': 'CONTINUE',  # Action to take if the step fails (CONTINUE or TERMINATE_CLUSTER)
        'HadoopJarStep': {  # Configuration for the step
            'Jar': 'command-runner.jar',  # Built-in EMR jar to run commands
            'Args': [  # Arguments for the command
                'spark-submit',  # Command to submit a Spark job
                '--deploy-mode',  # Deployment mode for the Spark job
                'cluster',  # Run the job on the EMR cluster
                's3://pyspark-code-gds-new/s3_to_hive_spark.py',  # Path to the PySpark script in S3
            ],
        }, 
    }],
    dag=dag,  # Associate this task with the defined DAG
)

# Define the task to monitor the status of the EMR step
step_checker = EmrStepSensor(
    task_id='check_step',  # Unique identifier for this task
    job_flow_id='j-27VNZHQ1YT7OW',  # The ID of the EMR cluster where the step is running
    step_id="{{ task_instance.xcom_pull(task_ids='add_step', key='return_value')[0] }}",  
    # Dynamically fetch the step ID from the output of the 'add_step' task using XCom
    aws_conn_id='aws_default',  # Connection ID for AWS credentials configured in Airflow
    poke_interval=120,  # Time interval (in seconds) to check the step status (2 minutes)
    timeout=86400,  # Maximum time (in seconds) to wait for the step to complete (1 day)
    mode='poke',  # Sensor mode; 'poke' checks periodically, while 'reschedule' frees up resources
    dag=dag,  # Associate this task with the defined DAG
)

# Define the task dependencies
step_adder >> step_checker  # The 'check_step' task will run after the 'add_step' task