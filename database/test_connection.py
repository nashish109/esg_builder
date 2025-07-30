import sys
import os
from sqlalchemy.exc import OperationalError

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import engine, SessionLocal
from config.settings import SQLALCHEMY_DATABASE_URL

def test_db_connection():
    """Tests the connection to the SQLite database."""
    print(f"Attempting to connect to the database...")
    print(f"  Database URL: {SQLALCHEMY_DATABASE_URL}")
    
    try:
        # The engine connects lazily. To check the connection, we need to perform an operation.
        connection = engine.connect()
        print("Successfully connected to the database engine.")
        
        # Test creating a session
        db = SessionLocal()
        print("Successfully created a database session.")
        
        # Perform a simple query to ensure the connection is truly working
        db.execute("SELECT 1")
        print("Successfully executed a test query.")
        
        connection.close()
        db.close()
        print("\nDatabase connection test successful!")
        
    except OperationalError as e:
        print("\n--- DATABASE CONNECTION FAILED ---")
        print(f"Error: {e}")
        print("\nTroubleshooting steps:")
        print("1. Ensure the file path for the SQLite database is correct.")
        print("2. Check for file permissions issues in the project directory.")
        
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    test_db_connection()