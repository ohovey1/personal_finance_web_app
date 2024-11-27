from flask_login import UserMixin
from .portfolio import Portfolio
from ..database.db_connection import DatabaseConnection

class User(UserMixin):
    def __init__(self, user_id, name, email):
        self.id = user_id  # Flask-Login requires this to be named 'id'
        self.name = name
        self.email = email
        self.portfolio = Portfolio()
        self.db = DatabaseConnection()

    def save(self, password):
        """Save user to database"""
        try:
            query = """
            INSERT INTO Users (name, email, password, created_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING user_id;
            """
            result = self.db.execute_query(query, (self.name, self.email, password))
            print(f"Database result: {result}")  # Debug print
            
            if result:
                self.id = result[0]['user_id']
                return True
            return False
                
        except Exception as e:
            print(f"Save error: {str(e)}")
            return False

    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        db = DatabaseConnection()
        query = "SELECT user_id, name, email FROM Users WHERE email = %s;"
        result = db.execute_query(query, (email,))
        if result:
            user_data = result[0]
            return cls(
                user_id=user_data['user_id'],
                name=user_data['name'],
                email=user_data['email']
            )
        return None

    @classmethod
    def get_by_id(cls, user_id):
        """Get user by ID"""
        db = DatabaseConnection()
        query = "SELECT user_id, name, email FROM Users WHERE user_id = %s;"
        result = db.execute_query(query, (user_id,))
        if result:
            user_data = result[0]
            return cls(
                user_id=user_data['user_id'],
                name=user_data['name'],
                email=user_data['email']
            )
        return None

    def verify_password(self, password):
        """Verify password"""
        query = "SELECT password FROM Users WHERE user_id = %s;"
        result = self.db.execute_query(query, (self.id,))
        if result:
            stored_password = result[0]['password']
            return stored_password == password  # Direct comparison
        return False

    def update_last_login(self):
        """Update last login timestamp"""
        query = "UPDATE Users SET last_login = CURRENT_TIMESTAMP WHERE user_id = %s;"
        self.db.execute_query(query, (self.id,))