from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from ..models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user alredy authenticated, go to portfolio dashboard
    if current_user.is_authenticated:
        return redirect(url_for('portfolio.view_portfolio'))
        
    # If not registered, take in email and password as inputs
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Get user from DB
        user = User.get_by_email(email)

        # Login if password verified, redirect to portfolio view
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('portfolio.view_portfolio'))
        
        # If invalid email or password, redirects back to login
        return render_template('auth/login.html', error="Invalid email or password")
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Login page. Takes name, email, password
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email already registered
        if User.get_by_email(email):
            return render_template('auth/register.html', error="Email already registered")
        
        user = User(user_id=None, name=name, email=email)
        if user.save(password):
            login_user(user)
            return redirect(url_for('portfolio.view_portfolio'))
        
        return render_template('auth/register.html', error="Could not create account")
    
    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))