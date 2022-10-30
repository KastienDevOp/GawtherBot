import sqlite3 as sql

def create_db():
    with sql.connect('members.db') as mdb:
        cur = mdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS members(
            id INTEGER,
            bank INTEGER,
            quote TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS reports(
            id INTEGER,
            member TEXT,
            author TEXT,
            date TEXT,
            reason TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS suggestions(
            id INTEGER,
            member TEXT,
            date TEXT,
            description TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS appeals(
            id INTEGER,
            member TEXT,
            staff TEXT,
            date TEXT,
            notes TEXT
        )''')

    with sql.connect('config.db') as cfdb:
        cur = cfdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS rules(
            id INTEGER,
            author TEXT,
            editor TEXT,
            rule TEXT,
            date_last_edited TEXT
        )''')

    with sql.connect('bank.db') as bdb:
        cur = bdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS bank_transactions(
            id INTEGER,
            payer INTEGER,
            payee INTEGER,
            date TEXT,
            amount INTEGER,
            reason TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS bank_requests(
            id INTEGER,
            payer INTEGER,
            payee INTEGER,
            amount INTEGER,
            date TEXT,
            reason TEXT,
            paid TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS bank_adjustment_logs(
            id INTEGER,
            staff INTEGER,
            member INTEGER,
            amount INTEGER,
            method TEXT,
            reason TEXT,
            date TEXT
        )''')