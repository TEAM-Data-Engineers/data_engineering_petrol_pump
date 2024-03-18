from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.bash import BashSensor
from airflow.utils.trigger_rule import TriggerRule


default_args = {

    'owner': 'airflow',

    'depends_on_past': False,

    'start_date': datetime(2024, 3, 16),

    'email_on_failure': False,

    'email_on_retry': False,

    'retries': 0,
    
    'execution_timeout': timedelta(minutes=7)

}



dag = DAG(

    'pp_loc_airflow_new',

    default_args=default_args,

    description='A DAG to execute a bash script',

    schedule_interval='@daily',  # Define your desired schedule here

)



# Define your bash command here

bash_command_up = 'timeout 5m docker-compose -f /media/sf_data_engineering/group_project/data_engineering_petrol_pump/docker_scripts/docker-compose-petrol-pump.yaml up'   



# Define the BashOperator to execute the bash script

execute_bash_script = BashOperator(

    task_id='docker_compose_up',
    

    bash_command=bash_command_up,

    dag=dag,

)

bash_command_down = 'timeout 5m docker-compose -f /media/sf_data_engineering/group_project/data_engineering_petrol_pump/docker_scripts/docker-compose-petrol-pump.yaml down --remove orphans'   


execute_bash_exit = BashOperator(task_id="docker_compose_down", bash_command=bash_command_down,dag=dag ,     trigger_rule=TriggerRule.ONE_FAILED,)


execute_bash_script >> execute_bash_exit



