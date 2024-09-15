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
