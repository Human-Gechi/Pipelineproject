#Importing necessary libraries for the=is task
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logsfolder.logger import logger
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY") #loading API as a Global variable
URL = "https://newsapi.org/v2/top-headlines" #API endpoint

class NEWS:
    """Class News for extracting data"""
    def __init__(self):
        self.api_key = API_KEY # Attribute api_key

    def fetch_category(self, category, page_size=100): #Method for fetching data
            unique_articles = [] #list of articles
            seen_titles = set() # Making sure only unique articles are added
            page = 1
            #while loop for extracting json data
            while True:
                params = { #parameters for the api endpoint
                    "country": "us",
                    "category": category,
                    "pageSize": page_size,
                    "page": page,
                    "apiKey": self.api_key,
                }
                response = requests.get(URL, params=params) #Making a request to the API
                if response.status_code != 200: # Catching error in cases where statuscode != 200
                    logger("Error:", response.status_code, response.text) # Logger message for this error
                    break # sstopping the process

                data = response.json()# Getting the Json Data
                articles = data.get("articles", []) # Accesing the list that houses the parameters i seek

                for article in articles: #looping through each articles in a particular page
                    title = article.get("title", "").strip() #Acessing it's articles
                    if title and title not in seen_titles:
                        unique_articles.append(article) # Appending each articles into the list of articles
                        seen_titles.add(title) #Checking for duplicated articles

                if not articles:
                    break
                if len(articles) < page_size:
                    break
                page += 1
            return unique_articles