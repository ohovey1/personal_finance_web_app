from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from ..models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.get_by_email(email)
        if user and user.verify_password(password):
            login_user(user)
            user.update_last_login()
            return redirect(url_for('home'))
        
        return render_template('auth/login.html', error="Invalid email or password")
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"Registration attempt - Email: {email}")  # Debug
        
        user = User(user_id=None, name=name, email=email)
        save_success = user.save(password)
        print(f"Save success: {save_success}, User ID: {user.id}")  # Debug
        
        if save_success:
            login_success = login_user(user)
            print(f"Login success: {login_success}")  # Debug
            return redirect(url_for('home'))
        
        return render_template('auth/register.html', error="Could not create account")

    return render_template('auth/register.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))