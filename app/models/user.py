from flask_login import UserMixin
from .portfolio import Portfolio
from ..database.db_connection import DatabaseConnection

class User(UserMixin):
    def __init__(self, user_id: int, name: str, email: str):
        self.id = user_id  # Flask-Login requires this to be named 'id'
        self.name = name
        self.email = email
        self.portfolio = None  # Will be loaded when needed
        self.db = DatabaseConnection()

    def save(self, password: str) -> bool:
        """Save user to database and create portfolio"""
        try:
            # Save user
            query = """
            INSERT INTO Users (name, email, password)
            VALUES (%s, %s, %s)
            RETURNING user_id;
            """
            result = self.db.execute_query(query, (self.name, self.email, password))
            
            if result:
                self.id = result[0]['user_id']
                # Create portfolio for user
                self.portfolio = Portfolio(user_id=self.id)
                self.portfolio.save()
                return True
            return False
        except Exception as e:
            print(f"Error saving user: {str(e)}")
            return False

    @classmethod
    def get_by_email(cls, email: str):
        """Get user by email"""
        db = DatabaseConnection()
        query = "SELECT user_id, name, email FROM Users WHERE email = %s;"
        result = db.execute_query(query, (email,))
        
        if result:
            user_data = result[0]
            user = cls(
                user_id=user_data['user_id'],
                name=user_data['name'],
                email=user_data['email']
            )
            # Load user's portfolio
            user.portfolio = Portfolio.get_by_user_id(user.id)
            return user
        return None

    @classmethod
    def get_by_id(cls, user_id: int):
        """Get user by ID"""
        db = DatabaseConnection()
        query = "SELECT user_id, name, email FROM Users WHERE user_id = %s;"
        result = db.execute_query(query, (user_id,))
        
        if result:
            user_data = result[0]
            user = cls(
                user_id=user_data['user_id'],
                name=user_data['name'],
                email=user_data['email']
            )
            # Load user's portfolio
            user.portfolio = Portfolio.get_by_user_id(user.id)
            if not user.portfolio:  # Create portfolio if doesn't exist
                user.portfolio = Portfolio(user_id=user.id)
                user.portfolio.save()
            return user
        return None

    def verify_password(self, password: str):
        """Verify password"""
        query = "SELECT password FROM Users WHERE user_id = %s;"
        result = self.db.execute_query(query, (self.id,))
        if result:
            stored_password = result[0]['password']
            return stored_password == password
        return False