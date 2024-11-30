# app/database/db_connection.py
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class DatabaseConnection:
    _instance = None
    _connection = None
    _cursor = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Establish database connection"""
        try:
            # Connect using info from config file
            self._connection = psycopg2.connect(
                dbname=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                host=Config.DB_HOST,
                port=Config.DB_PORT
            )
            self._cursor = self._connection.cursor(cursor_factory=RealDictCursor)
            print("Database connection successful!")
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query: str, params: tuple = None):
        """Execute a query and return results"""
        try:
            self._cursor.execute(query, params)
            if query.lower().startswith('select'):
                return self._cursor.fetchall()
            self._connection.commit()
            return self._cursor.fetchall() if self._cursor.description else True
        except Exception as e:
            self._connection.rollback()
            print(f"Query error: {str(e)}")
            return None

    def close(self):
        """Close database connection"""
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()
            print("Database connection closed.")

    def __del__(self):
        """Ensure connection is closed when object is deleted"""
        self.close()