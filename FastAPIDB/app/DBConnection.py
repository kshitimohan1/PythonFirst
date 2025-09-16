import psycopg2
from psycopg2.extras import RealDictCursor
import time

def get_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host='localhost',
                database='fastapi',
                user='postgres',
                password='Aqadmin@123',
                cursor_factory=RealDictCursor
            )
            conn.autocommit = True
            print("DB connection was Successful")
            return conn
        except Exception as error:
            print("Connecting to db failed")
            print("Error :", error)
            time.sleep(2)


def get_db_cursor():
    conn = get_connection()
    return conn, conn.cursor()