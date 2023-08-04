import sqlite3
import json
from sqlite3 import Error
from tabulate import tabulate
import pandas as pd
import os


def create_db():
    """ Create a database connection to a SQLite database. """
    try:
        connection = sqlite3.connect('workers.db')

        # Create table for database
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT,
            working_week TEXT,
            schedule TEXT
            )
        """)
        connection.commit()
        return connection, cursor
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
    connection.close()


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
    new_schedule = {
        'Mon': '',
        'Tue': '',
        'Wed': '',
        'Thu': '',
        'Fri': ''
    }

    # Ask for which week changes should be made
    print(get_week(name))
    choice = int(input('Select id of week which you want to edit: '))

    #wyczysc tutaj i wpisz schedule na ten tydzien

    # Iterate through week and ask for changes
    for day in new_schedule:
        new_shift = input(f'Provide new schedule for {day}: ')
        new_schedule[day] = new_shift

    schedule_json = json.dumps(new_schedule)
    cursor.execute("""
        UPDATE workers
        SET schedule = ?
        WHERE name = ? AND id = ?;
    """, (schedule_json, name, choice))
    connection.commit()
    connection.close()


def get_week(name):
    connection, cursor = create_db()
    query = ("SELECT id, working_week FROM workers")
    df = pd.read_sql(query, connection)
    connection.close()
    show = tabulate(df, headers='keys')
    return show
