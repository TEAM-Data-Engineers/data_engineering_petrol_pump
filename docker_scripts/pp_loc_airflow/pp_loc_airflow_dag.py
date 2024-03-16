from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 16),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'execute_bash_script',
    default_args=default_args,
    description='A DAG to execute a bash script',
    schedule_interval='@daily',  # Define your desired schedule here
)

# Define your bash command here
bash_command = '/media/sf_data_engineering/group_project/data_engineering_petrol_pump/docker_scripts/docker_run.sh'

# Define the BashOperator to execute the bash script
execute_bash_script = BashOperator(
    task_id='execute_bash_script',
    bash_command=bash_command,
    dag=dag,
)
