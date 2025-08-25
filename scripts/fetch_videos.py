import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sql.tables import DBLoader, DBTableManager
from logsfolder.logger import logger
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "https://newsapi.org/v2/top-headlines"

class NEWS:
    def __init__(self):
        self.api_key = API_KEY

    def fetch_category(self, category, page_size=100):
            unique_articles = []
            seen_titles = set()
            page = 1

            while True:
                params = {
                    "country": "us",
                    "category": category,
                    "pageSize": page_size,
                    "page": page,
                    "apiKey": self.api_key,
                }
                response = requests.get(URL, params=params)
                if response.status_code != 200:
                    logger("Error:", response.status_code, response.text)
                    break

                data = response.json()
                articles = data.get("articles", [])

                for article in articles:
                    title = article.get("title", "").strip()
                    if title and title not in seen_titles:
                        unique_articles.append(article)
                        seen_titles.add(title)

                if not articles:
                    break
                if len(articles) < page_size:
                    break
                page += 1
            return unique_articles
