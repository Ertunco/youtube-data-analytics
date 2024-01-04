"""
This script creates a DAG named youtube_data_collection that runs once a day.
It includes a single task (fetch_data_task) that executes the fetch_youtube_data function.
This function uses the YouTube Data API to fetch data about the most popular videos in Turkey.
"""

import os
from datetime import datetime, timedelta, date
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
from googleapiclient.discovery import build
load_dotenv()

# Set dataframe max row display
pd.set_option('display.max_row', 10)

# Set dataframe max column width to 20
pd.set_option('display.max_columns', 20)


# YouTube API Setup
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_API_KEY = os.getenv('youtubeAPI')
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

def fetch_youtube_data():
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="TR",
        maxResults=50
    )
    response = request.execute()

    # Add your logic here to handle the response, like saving it to a database

# Default args for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'youtube_data_collection',
    default_args=default_args,
    description='DAG for fetching YouTube data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Define the task
fetch_data_task = PythonOperator(
    task_id='fetch_youtube_data',
    python_callable=fetch_youtube_data,
    dag=dag,
)

fetch_data_task