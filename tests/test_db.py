# tests/test_db.py
from app.database.db_connection import DatabaseConnection

def test_connection():
    try:
        db = DatabaseConnection()
        # Test a simple query
        db.execute_query("SELECT version();")
        print("Database connection test successful!")
    except Exception as e:
        print(f"Database connection test failed: {e}")

if __name__ == "__main__":
    test_connection()