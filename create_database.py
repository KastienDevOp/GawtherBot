import sqlite3 as sql

def create_db():
    with sql.connect('main.db') as mdb:
        cur = mdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS members(
            id INTEGER,
            quote TEXT,
            mutes INTEGER,
            bans INTEGER,
            warnings INTEGER,
            kicks INTEGER,
            bank INTEGER
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER,
            payer INTEGER,
            payee INTEGER,
            date INGEGER,
            amount INTEGER,
            reason TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS requests(
            id INTEGER,
            payer INTEGER,
            payee INTEGER,
            date TEXT,
            amount INTEGER,
            reason TEXT,
            paid TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS reports(
            id INTEGER,
            type TEXT,
            title TEXT,
            details TEXT,
            date TEXT,
            author INTEGER
        )''')
