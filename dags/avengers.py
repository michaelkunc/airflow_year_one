"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2018, 7, 9),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
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
t5 = BashOperator(task_id="email_aggregate_excel", bash_command="echo send that spreadsheet!", retries=3, dag=example_bash)

# set execution order
t1 >> t2 >> t3
t2 >> t4
t3 >> t5


dag = DAG("avengers-bash", default_args=default_args, schedule_interval=timedelta(1))
