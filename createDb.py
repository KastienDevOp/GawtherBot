import sqlite3 as sql

def create_db():
    with sql.connect('bank.db') as mdb:
        cur = mdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS transactions(
            transaction_number INTEGER,
            payer INTEGER,
            payee INTEGER,
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

        cur.execute('''CREATE TABLE IF NOT EXISTS adjustments(
            adjustment_number INTEGER,
            staff INTEGER,
            member INTEGER,
            amount INTEGER,
            method TEXT,
            reason TEXT,
            date TEXT
        )''')

    with sql.connect('members.db') as mdb:
        cur = mdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS profiles(
            member INTEGER,
            bank INTEGER,
            quote TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS reports(
            report_number INTEGER,
            date TEXT,
            staff INTEGER,
            member INTEGER,
            type TEXT,
            total_time INTEGER,
            reason TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS suggestions(
            suggestion_number INTEGER,
            member INTEGER,
            date TEXT,
            details TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS appeals(
            appeal_number INTEGER,
            member INTEGER,
            date TEXT,
            staff INTEGER,
            decision TEXT,
            reason_appeal TEXT,
            reason_decision TEXT
        )''')

    with sql.connect('rules.db') as mdb:
        cur = mdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS current(
            rule_number INTEGER,
            rule_name TEXT,
            rule_details TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS edits(
            rule_number INTEGER,
            prev_rule_name TEXT,
            new_rule_name TEXT,
            prev_rule_details TEXT,
            new_rule_details TEXT,
            staff INTEGER,
            reason TEXT,
            date TEXT
        )''')