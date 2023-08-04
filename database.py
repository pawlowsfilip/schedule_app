import sqlite3
import json
from sqlite3 import Error
from tabulate import tabulate
import pandas as pd


def create_db():
    """ Create a database connection to a SQLite database. """
    try:
        conn = sqlite3.connect('workers.db')

        # Create table for database
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workers (
            name TEXT,
            position TEXT,
            working_week TEXT,
            schedule TEXT
            )
        """)
        conn.commit()
        return conn, cursor
    except Error as e:
        print(e)


def insert_schedule(worker):
    """ Insert the data to SQL database. Schedule_json for converting the schedule to list. """
    connection, cursor = create_db()
    schedule_json = json.dumps(worker.schedule)

    cursor.execute("""
        INSERT INTO workers (name, position, working_week, schedule)
        VALUES (?, ?, ?, ?)
    """, (worker.name, worker.position, worker.working_week, schedule_json))
    connection.commit()


def get_schedule(name):
    connection, cursor = create_db()
    cursor.execute("""
        SELECT schedule FROM workers WHERE name = ?
    """, (name,))
    schedule_json = cursor.fetchone()[0]
    return json.loads(schedule_json)


def get_db():
    connection, cursor = create_db()
    query = "SELECT * FROM workers"
    df = pd.read_sql(query, connection)
    connection.close()
    show = tabulate(df, headers='keys')
    return show


def edit_schedule(name):
    connection, cursor = create_db()
    new_data = input('Provide new schedule: ')

