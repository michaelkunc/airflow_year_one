from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2018, 7, 14),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

# example dag
example_bash = DAG("example-bash", default_args=default_args)

# example tasks
t1 = BashOperator(task_id="extract", bash_command="echo extracting data!", dag=example_bash)
t2 = BashOperator(task_id="load_to_s3", bash_command="echo load to S3!", retries=3, dag=example_bash)
t3 = BashOperator(task_id="aggregate", bash_command="echo aggregating data!", retries=3, dag=example_bash)
t4 = BashOperator(task_id="transfer_raw_data", bash_command="echo transfer!", retries=3, dag=example_bash)
t5 = BashOperator(
    task_id="email_aggregate_excel", bash_command="echo send that spreadsheet!", retries=3, dag=example_bash
)

# set execution order
t1 >> t2 >> t3
t2 >> t4
t3 >> t5


# Python example

import random
import time

avengers_python = DAG("avengers", default_args=default_args, schedule_interval="@hourly")

AVENGERS = ("Hulk", "Black Widow", "Hawkeye", "Iron Man", "Thor", "Black Panther", "Captain America")

ENEMIES = ("The Puppet Master", "M.O.D.O.K.", "Ultron", "Green Goblin")


def get_team():
    time.sleep(random.randint(1, 3))  
    return random.sample(AVENGERS, 4)


def get_location():
    time.sleep(random.randint(1, 5))  
    return random.sample(["New York", "Los Angeles", "Outer Space"], 1)


def get_enemy():
    time.sleep(random.randint(10, 25))  
    return random.sample(ENEMIES, 1)



team = PythonOperator(task_id="select_avengers", python_callable=get_team, dag=avengers_python)

location = PythonOperator(task_id="select_location", python_callable=get_location, dag=avengers_python)

enemies = PythonOperator(task_id="get_enemy", python_callable=get_enemy, dag=avengers_python)

# execution order
team >> location >> enemies
