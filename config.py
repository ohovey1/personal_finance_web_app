# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    DB_NAME = "portfolio_management"
    DB_USER = "postgres"
    DB_PASSWORD = "Likliklik35!"
    DB_HOST = "localhost"
    DB_PORT = "5432"