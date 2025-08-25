from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG('my_dag', start_date=datetime(2025, 8, 25), schedule_interval='@daily')

task = BashOperator(
    task_id='run_script',
    bash_command="C:\\Users\\HP\\OneDrive\\Desktop\\Youtubeapi\\scripts\\load_to_db.py",
    dag=dag
)
