import sqlite3
from lib.db.connection import get_connection

def setup_schema():
    """
    Sets up the database schema by creating the necessary tables.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create authors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')

        # Create magazines table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        ''')

        # Create articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
                FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        # print("Database schema set up successfully!") # Comment out for cleaner test output

if __name__ == '__main__':
    setup_schema()