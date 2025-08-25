import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import sys
from psycopg2 import IntegrityError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logsfolder.logger import logger
class DBConnection:
    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        logger.info("Database connection established.")
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def execute(self, sql, params=None, commit: bool = True):
        self.cursor.execute(sql, params or ())
        if commit:
            self.conn.commit()
    def close(self):
        self.cursor.close()
        self.conn.close()

class DBTableManager(DBConnection):
    def __init__(self):
        super().__init__()
    def create_table(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS entertainment(
                name TEXT,
                title TEXT,
                description TEXT,
                UNIQUE(description,title),
                publishedAt TIMESTAMP
            );
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS science(
                name TEXT,
                title TEXT,
                description TEXT,
                UNIQUE(description,title),
                publishedAt TIMESTAMP
            );
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS technology(
                name TEXT,
                title TEXT,
                description TEXT,
                UNIQUE(description,title),
                publishedAt TIMESTAMP
            );
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS health(
                name TEXT,
                title TEXT,
                description TEXT,
                UNIQUE(title, description),
                publishedAt TIMESTAMP
            );
        """)
        print("✅ Tables created successfully!")
        logger.info("Tables created successfully!")
class DBLoader(DBConnection):
    def __init__(self):
        super().__init__()
    def insert_articles(self, category, articles):
        table_map = {
            "science": "science",
            "health": "health",
            "technology": "technology",
            "entertainment": "entertainment"
        }
        table_name = table_map.get(category)
        if not table_name:
            return
        for article in articles:
            try:
                self.cursor.execute(
                    f"""
                    INSERT INTO {table_name} (name, title, description, publishedAt)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (article['source']['name'], article['title'], article['description'], article['publishedAt'])
                )
            except IntegrityError:
                # Ignore Duplicates by rolling back the transaction
                self.conn.rollback()
                logger.warning(f"Duplicate articles found in {table_name} table. Skipping insertion.")
        self.conn.commit()
