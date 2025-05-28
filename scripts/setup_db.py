from lib.db.connection import get_connection

def setup_database():
    with get_connection() as conn:
        with open('lib/db/schema.sql') as f:
            conn.executescript(f.read())
        conn.commit()

if __name__ == "__main__":
    setup_database()
    print("Database tables created")