import mysql.connector
import os
from dotenv import load_dotenv 
from functools import wraps


def connect():
    load_dotenv()    
    return mysql.connector.connect(
      host=os.getenv("DB_HOST"),
      user=os.getenv("DB_USER"),
      password=os.getenv("DB_PASSWORD"),
      database=os.getenv("DB_NAME")
    )


def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = connect()
        cursor = db.cursor(dictionary=True)
        
        kwargs['cursor'] = cursor
        kwargs['db'] = db
        
        try:
            result = func(*args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

    return wrapper


def get_member_rank(cursor, name):
    query = "SELECT * FROM members ORDER BY elo DESC;"
    cursor.execute(query)
    members = cursor.fetchall()

    for i, member in enumerate(members):
        if member["name"] == name:
            return i + 1


def get_member_by_name(cursor, name):
    query = "SELECT * FROM members WHERE name = %s;"
    cursor.execute(query, (name,))
    return cursor.fetchone()


def update_member_elo(db, cursor, member_id, new_elo):
    update_query = "UPDATE members SET elo = %s WHERE id = %s;"
    cursor.execute(update_query, (new_elo, member_id))
    db.commit()
