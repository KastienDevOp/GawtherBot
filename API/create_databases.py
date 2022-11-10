import sqlite3 as sql

def brain():
    executes = [
        create_members,
        create_rules,
        create_banks,
        create_reports,
        create_quotes
    ]

    print("Creating Databi. . . Please Wait. . .")

    for i in executes:
        try:
            i()
        except:
            print("Database Already Exists")

        print(i, " Executed Successfully.")

    print("All Databi Have Been Created.")

def create_members():
    with sql.connect('./databases/members.db') as mdb:
        cur = mdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS profile(
            id INTEGER,
            quote TEXT,
            mutes INTEGER,
            bans INTEGER,
            warnings INTEGER,
            kicks INTEGER,
            dob TEXT,
            color TEXT,
            bank INTEGER
        )''')

def create_rules():
    with sql.connect('./databases/rules.db') as rdb:
        cur = rdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS rules(
            id INTEGER,
            name TEXT,
            details TEXT,
            edited TEXT,
            staff TEXT,
            reason TEXT,
            date TEXT
        )''')

def create_banks():
    with sql.connect('./databases/bank.db') as bdb:
        cur = bdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER,
            payer INTEGER,
            payee INTEGER,
            type TEXT,
            method TEXT,
            date TEXT,
            amount INTEGER,
            reason TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS requests(
            request_number INTEGER,
            payer INTEGER,
            payee INTEGER,
            date TEXT,
            amount INTEGER,
            reason TEXT,
            paid TEXT
        )''')

def create_reports():
    with sql.connect('./databases/reports.db') as redb:
        cur = redb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS reports(
            id INTEGER,
            type TEXT,
            date TEXT,
            author INTEGER,
            member INTEGER,
            time INTEGER,
            reason TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS suggestions(
            id INTEGER,
            author INTEGER,
            date TEXT,
            title TEXT,
            description TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS appeals(
            id INTEGER,
            author INTEGER,
            date TEXT,
            staff INTEGER,
            decision TEXT,
            reason_appeal TEXT,
            reason_decision TEXT
        )''')

def create_quotes():
    with sql.connect('./databases/quotes.db') as qdb:
        cur = qdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS quotes(
            id INTEGER,
            author TEXT,
            quote TEXT
        )''')