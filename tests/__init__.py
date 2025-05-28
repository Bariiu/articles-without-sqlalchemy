import os
import sqlite3
import pytest
from lib.db.connection import get_connection
from lib.db.schema import setup_schema

DB_PATH = 'lib/db/database.db'

@pytest.fixture(scope="session", autouse=True)
def setup_database_file_and_schema():
    """
    Ensures a clean database file and schema before the entire test session.
    Runs once per test session.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    setup_schema() 
    
    yield

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

