
import os
from datetime import datetime, timedelta, date
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
load_dotenv()

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
    return response

response = fetch_youtube_data()
print(response)