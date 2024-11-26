# app/__init__.py
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    from app.database.db_connection import DatabaseConnection
    db = DatabaseConnection()

    # Register blueprints
    # from app.routes import auth_routes, portfolio_routes, account_routes
    # app.register_blueprint(auth_routes.bp)
    # app.register_blueprint(portfolio_routes.bp)
    # app.register_blueprint(account_routes.bp)

    # Test route
    @app.route('/')
    def home():
        return 'Portfolio Management App - Database Connection Successful!'
    return app