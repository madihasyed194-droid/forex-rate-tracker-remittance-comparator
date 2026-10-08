import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_NAME = os.path.join(BASE_DIR, "forex.db")


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_pair TEXT NOT NULL,
            rate REAL NOT NULL,
            rate_date TEXT NOT NULL,
            UNIQUE(currency_pair, rate_date)
        )
    """)

    connection.commit()
    connection.close()


def save_rate(currency_pair, rate, rate_date):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO exchange_rates
        (currency_pair, rate, rate_date)
        VALUES (?, ?, ?)
    """, (currency_pair, rate, rate_date))

    connection.commit()
    connection.close()


def get_rate_history():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT currency_pair, rate, rate_date
        FROM exchange_rates
        ORDER BY rate_date DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data