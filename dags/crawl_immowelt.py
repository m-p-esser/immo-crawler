import datetime
import asyncio

from airflow.sdk import dag
from airflow.providers.standard.operators.empty import EmptyOperator
from src.crawler.immowelt_bs4 import main


@dag(start_date=datetime.datetime(2021, 1, 1), schedule="@daily")
def generate_dag():
    EmptyOperator(task_id="task")
    asyncio.run(main())

generate_dag()
