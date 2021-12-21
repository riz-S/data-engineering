from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator

# Inisiasi default argumen ke tiap-tiap task
default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'email': ['riz_stwn@student.ub.ac.id'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# Membuat konfigurasi DAGnya
with DAG(
    'final-project-de',
    default_args=default_args,
    description='Final Project DE-B Klp 5',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2021, 12, 8),
    catchup=False,
    tags=['final-project'],
) as dag:
    # Inisialisasi task
    t1 = BashOperator(
        task_id='start_kafka',
        bash_command='/mnt/e/Projects/VisualStudio/PipelineStream/scripts/start_kafka.sh ',
    )

    t2 = BashOperator(
        task_id='etl',
        depends_on_past=False,
        bash_command='/mnt/e/Projects/VisualStudio/PipelineStream/scripts/etl.sh ',
        retries=3,
    )

    t3 = BashOperator(
        task_id='stop_kafka',
        depends_on_past=False,
        bash_command='/mnt/e/Projects/VisualStudio/PipelineStream/scripts/stop_kafka.sh ',
    )

    # Membuat urutan dari task
    t1 >> t2 >> t3