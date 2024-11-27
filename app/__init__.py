from flask import Flask, render_template
from flask_login import LoginManager
from config import Config

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Initialize database
    from app.database.db_connection import DatabaseConnection
    db = DatabaseConnection()

    # User loader for Flask-Login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

    # Home route
    @app.route('/')
    def home():
        return render_template('home.html')

    # Register blueprints
    from app.routes import auth_routes
    app.register_blueprint(auth_routes.bp)

    return app