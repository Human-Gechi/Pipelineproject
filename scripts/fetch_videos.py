from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
#Youtube client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

