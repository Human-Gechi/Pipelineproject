#Importing the necessary packeges
import psycopg2 # Postgres connection
import psycopg2.extras
from dotenv import load_dotenv #Loading environmental packages
import os #os module
import sys #sys module for accessing other folders in the parent directory
from psycopg2 import IntegrityError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logsfolder.logger import logger #Importing the logger variable from the logs folder
class DBConnection: #Database connection class
    """Class for Database Connection"""
    def __init__(self): #initalizing attributes
        load_dotenv() #loading env. variables for Db connection
        self.conn = psycopg2.connect( #connecting to the database using my credentials
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        ) #Makihng a valid Database connection
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        logger.info("Database connection established.") #Confirmation message for DB creation
    def query(self, sql, params=None): #query function praram
        self.cursor.execute(sql, params or ()) #Execution
        return self.cursor.fetchall() #Fetching data

    def execute(self, sql, params=None, commit: bool = True): #Function to execute a parameter
        self.cursor.execute(sql, params or ())
        if commit:
            self.conn.commit() # Commiting to the Database
    def close(self):
        self.cursor.close()
        self.conn.close()
# Table Manager class
class DBTableManager(DBConnection):
    """Class for Managing the creation of tables that inherits from the DBConnection class"""
    def __init__(self):
        super().__init__() # initializing the parent or super class
    def create_table(self):
        # Method for the creation of Tables
        self.execute(""" 
            CREATE TABLE IF NOT EXISTS entertainment(
                name TEXT,
                title TEXT,
                description TEXT,
                url TEXT PRIMARY KEY ,
                publishedAt TIMESTAMP
            );
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS science(
                name TEXT,
                title TEXT,
                description TEXT,
                url TEXT PRIMARY KEY ,
                publishedAt TIMESTAMP
            );
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS technology(
                name TEXT,
                title TEXT,
                description TEXT,
                url TEXT PRIMARY KEY ,
                publishedAt TIMESTAMP
            );
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS health(
                name TEXT,
                title TEXT,
                description TEXT,
                url TEXT PRIMARY KEY ,
                publishedAt TIMESTAMP
            );
        """)
        print("✅ Tables created successfully!") # Logger message for succesfully creating Tables
        logger.info("Tables created successfully!")
class DBLoader(DBConnection):
    """Class for loading content into Database that inherits from the Dbconnection class"""
    def __init__(self):
        super().__init__() # Initializing the Parent class
    def insert_articles(self, category, articles):#Method for inserint articles
        table_map = {#Dictionary for mapping a category in to it's table
            "science": "science",
            "health": "health",
            "technology": "technology",
            "entertainment": "entertainment",
        }
        table_name = table_map.get(category) # variable for mapping categories
        if not table_name:
            return#if the table name is not in these categories, return an empty dictionary
        insert_query = f"""
            INSERT INTO {table_name} (name, title, description,url,publishedAt)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING;
        """
        for article in articles: # Looping throught the list of dictionaries/Json data
            try: #Try except block for errors
                self.cursor.execute(insert_query, (#inserint into tables
                    article['source']['name'],
                    article['title'],
                    article['description'],
                    article['url'],
                    article['publishedAt']
                ))
            except Exception as e: #Errors catching
                self.conn.rollback() #Preventing an update incases of errors
                logger.error(f"Error inserting into {table_name}: {e}") # Logger message
            else:
                logger.info(f"Inserted article into {table_name}: {article['title']}") #Infor message for logs
        self.conn.commit()  #commiting the data

