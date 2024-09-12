import mysql.connector
import os
from dotenv import load_dotenv 

def connect():
    load_dotenv()    
    return mysql.connector.connect(
      host=os.getenv("DB_HOST"),
      user=os.getenv("DB_USER"),
      password=os.getenv("DB_PASSWORD"),
      database=os.getenv("DB_NAME")
    )

