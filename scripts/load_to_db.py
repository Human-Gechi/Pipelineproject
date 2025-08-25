import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sql.tables import DBLoader,DBTableManager
from scripts.fetch_videos import NEWS
from logsfolder.logger import logger

# Initializing database objects
DBTableManager().create_table()
logger.info("Database tables created or verified.")
db_loader = DBLoader()
news = NEWS()

article1 = news.fetch_category("science")
print(db_loader.insert_articles("science", article1))
logger.info(f"Inserting articles into database: {len(article1)} science articles found.")

article2 = news.fetch_category("technology")
print(db_loader.insert_articles("technology", article2))
logger.info(f"Inserting articles into database: {len(article2)} technology articles found.")

article3 = news.fetch_category("health")
print(db_loader.insert_articles("health", article3))
logger.info(f"Inserting articles into database: {len(article3)} health articles found.")

article4 = news.fetch_category("entertainment")
print(db_loader.insert_articles("entertainment", article4))
logger.info(f"Inserting articles into database: {len(article4)} entertainment articles found.")