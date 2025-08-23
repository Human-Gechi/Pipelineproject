from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("APIKEY")
class YoutubeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_key = API_KEY
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        #Youtube client
        self.youtube  = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=self.api_key)
        return self.youtube
    titlelist  = [
            "Snowflake", "Apache Airflow", "Orchestration", "data lakes",
            "Cloud data warehouses", "NoSQL", "Kafka", "Kinesis", "Spark", "PySpark",
            "ELT", "ETL", "streaming", "Visualizations", "batch processing", "stream processing"
        ]

class ChannelFetcher(YoutubeClient):
    def __init__(self, api_key):
        super().__init__(api_key)

    def get_channel_details(self):
        self.channel_ids = []
        self.channel_names = []

        for keyword in self.titlelist:
            request = self.youtube.search().list(
                part="snippet",
                q=keyword,
                maxResults=2,
                type="channel"
            )
            response = request.execute()

            for item in response.get("items", []):
                if item["id"]["kind"] == "youtube#channel":
                    channel_id = item["id"]["channelId"]
                    channel_name = item["snippet"]["channelTitle"]
                    self.channel_ids.append(channel_id)
                    self.channel_names.append(channel_name)

        return self.channel_ids, self.channel_names
class VideoFetcher(YoutubeClient):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.channel_fetcher = ChannelFetcher(api_key)  # composition
        self.video_ids = []
        self.video_names = []
        self.published_times = []
        self.channel_match = []

    def video_channel_playlist(self):
        # fetch channels first
        self.channel_fetcher.get_channel_details()

        for keyword in self.titlelist:
            request = self.youtube.search().list(
                part="snippet",
                q=keyword,
                maxResults=1,
                type="video"
            )
            response = request.execute()

            for item in response.get("items", []):
                if item["id"]["kind"] == "youtube#video" and \
                   item["snippet"]["channelId"] in self.channel_fetcher.channel_ids:

                    self.video_ids.append(item["id"]["videoId"])
                    self.video_names.append(item["snippet"]["title"])
                    self.published_times.append(item["snippet"]["publishTime"])
                    self.channel_match.append(item["snippet"]["channelId"])

        return self.channel_match, self.video_ids, self.video_names, self.published_times

class SuscriberCont(YoutubeClient):
    def __init__(self, api_key):
        super().__init__(api_key)
    def channel_stat(self):
        for keyword in self.titlelist:
            request = self.youtube.channel().list(
                part="snippet",
                q=keyword,
                maxResults=""
            )
        response = request.execute()
        self.suscribecount =[]
        for item in response.get('items', []):
            if item["statistics"]:
                suscribers = item['statistics']['suscriberCount']
                self.suscribecount.append(suscribers)
        return self.suscribecount
you = VideoFetcher(api_key=API_KEY)
print(you.video_channel_playlist())