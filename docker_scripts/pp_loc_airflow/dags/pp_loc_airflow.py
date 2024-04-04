from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.bash import BashSensor
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.generic_transfer import GenericTransfer
from airflow.operators.postgres_operator import PostgresOperator
from airflow.sensors.time_delta_sensor import TimeDeltaSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.python import PythonSensor
import time

default_args = {

    'owner': 'airflow',

    'depends_on_past': False,

    'start_date': datetime(2024, 3, 24),

    'email_on_failure': False,

    'email_on_retry': False,

    'retries': 0,
    
    'execution_timeout': timedelta(minutes=10) ,
    
    'catchup': False

}

#### Script paths Start ###
docker_to_stg_prod_path = 'sql/pp_locations_docker_to_stage.sql'
ppl_stg_to_prod_path = 'sql/pp_locations_stage_to_prod.sql'
execute_bash_script_path = 'bash/docker_up.sh'
execute_bash_exit_path = 'bash/docker_down.sh'
pg_dump_bash_path = 'bash/pg_dump_dbt.sh'
pp_pg_restore_sql_path = 'sql/pp_pg_restore.sql'
#### Script paths End ###

dag = DAG(

    'pp_loc_airflow',

    default_args=default_args,

    description='A DAG to execute a bash script',

    schedule_interval='@daily',  # Define your desired schedule here

)


########START OF execute_bash_script #########################

# Define your bash command here
# Define the BashOperator to execute the bash script

execute_bash_script = BashOperator(

    task_id='docker_compose_up',
    bash_command=execute_bash_script_path,
    dag=dag

)


########END OF execute_bash_script #########################


########START  OF BASH COMMAND DOWN#########################

execute_bash_exit = BashOperator(
	task_id="docker_compose_down", 
	bash_command=execute_bash_exit_path,
	dag=dag
	)


########END  OF BASH COMMAND DOWN#########################


pg_dump_bash = BashOperator(

    task_id='pg_dump_bash',
    bash_command=pg_dump_bash_path,
    dag=dag

)


pg_restore_sql = PostgresOperator(

    task_id='pg_restore_sql',
    postgres_conn_id='prod_de_db',  # Connection ID defined in Airflow Admin
    sql= pp_pg_restore_sql_path,  # SQL query to execute
    dag=dag

)

####START OF docker_to_stg_prod ################



docker_to_stg_prod = PostgresOperator(
        task_id='docker_to_stg_prod',
        postgres_conn_id='prod_de_db',  # Connection ID defined in Airflow Admin
        sql= docker_to_stg_prod_path,  # SQL query to execute
        dag=dag
        #trigger_rule=TriggerRule.ONE_FAILED
    )

####END OF docker_to_stg_prod ################

####START OF ppl_stg_to_prod ################

ppl_stg_to_prod = PostgresOperator(
        task_id='ppl_stg_to_prod',
        postgres_conn_id='prod_de_db',  # Connection ID defined in Airflow Admin
        sql=ppl_stg_to_prod_path,  # SQL query to execute
        #dag=dag
        #trigger_rule=TriggerRule.ONE_FAILED
    )

####END OF ppl_stg_docker_to_stg_prod ################


def wait_function():
    # Sleep for 300 seconds (5 minutes)
    time.sleep(240)
    return True  # Signal that the condition is met

wait_task_db = PythonSensor(
        task_id='wait_task_db',
        python_callable=wait_function,
        mode='poke',
        timeout=600,  # Timeout after 10 minutes if condition is not met
        poke_interval=30,  # Check every 30 seconds
        dag=dag
    )

wait_task_docker = TimeDeltaSensor(
        task_id='wait_task_docker',
        delta=timedelta(minutes=1),
        mode='poke' 
#        dag=dag ,
    )

start_task = DummyOperator(
			    task_id='start_task',
			    dag=dag								
			  )


[ execute_bash_script ]
#[wait_task_docker >> ]
[start_task >> wait_task_db >> docker_to_stg_prod >> ppl_stg_to_prod >> execute_bash_exit]
[start_task >> wait_task_db >> pg_dump_bash >> pg_restore_sql]
