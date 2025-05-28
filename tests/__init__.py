import os
import sqlite3
import pytest
from lib.db.connection import get_connection
from lib.db.schema import setup_schema

# Define the path to your test database
DB_PATH = 'lib/db/database.db' # Make sure this matches the path used in connection.py

@pytest.fixture(scope="session", autouse=True)
def setup_database_file_and_schema():
    """
    Ensures a clean database file and schema before the entire test session.
    Runs once per test session.
    """
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Remove the database file if it exists to start fresh for the session
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Set up the schema using your setup_schema function
    setup_schema() 
    
    yield # This yields control to the tests. Code after yield runs as teardown.

    # Teardown: Clean up the database file after the entire test session
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

# The individual test files will have their own autouse fixture to clear data per test.