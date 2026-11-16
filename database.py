import os
import sqlite3

# Always use the one shared database stored beside this file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "livestock.db")


def get_db_connection():
    """Return a connection to the common livestock database."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Create the three agreed tables if they do not already exist."""
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_type TEXT NOT NULL,
            breed TEXT NOT NULL,
            age INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("livestock.db and the shared tables are ready!")
