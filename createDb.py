import sqlite3 as sql

def create_db():
    with sql.connect('main.db') as mdb:
        cur = mdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS members(
            id INTEGER PRIMARY KEY,
            bank INTEGER
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS reports(
            id INTEGER PRIMARY KEY,
            member TEXT,
            author TEXT,
            date TEXT,
            reason TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS suggestions(
            id INTEGER PRIMARY KEY,
            member TEXT,
            date TEXT,
            description TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS appeals(
            id INTEGER PRIMARY KEY,
            member TEXT,
            staff TEXT,
            date TEXT,
            notes TEXT
        )''')