
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from replit import db
import hashlib
import os
from datetime import datetime

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

# Helper function to hash passwords
def hash_password(password):
    salt = os.environ.get('PASSWORD_SALT', 'mystic_arcana_salt')
    return hashlib.sha256((password + salt).encode()).hexdigest()

@profile_bp.route('/')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    user = db['users'].get(session['user_id']) if 'users' in db else None
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('profile.login'))
    
    return render_template('profile.html', user=user)

@profile_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if 'users' not in db:
            flash('Invalid email or password', 'error')
            return render_template('login.html')
        
        user_id = None
        for uid, user_data in db['users'].items():
            if user_data.get('email') == email and user_data.get('password') == hash_password(password):
                user_id = uid
                break
        
        if user_id:
            session['user_id'] = user_id
            return redirect(url_for('profile.profile'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@profile_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not name or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        # Check if email already exists
        if 'users' in db:
            for user_data in db['users'].values():
                if user_data.get('email') == email:
                    flash('Email already registered', 'error')
                    return render_template('register.html')
        else:
            db['users'] = {}
        
        # Create new user
        user_id = str(datetime.now().timestamp())
        db['users'][user_id] = {
            'id': user_id,
            'name': name,
            'email': email,
            'password': hash_password(password),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'preferences': {
                'zodiac_sign': None,
                'notifications': True
            }
        }
        
        session['user_id'] = user_id
        return redirect(url_for('profile.profile'))
    
    return render_template('register.html')

@profile_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home.home'))

@profile_bp.route('/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    user = db['users'].get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('profile.login'))
    
    # Update user info
    user['name'] = request.form.get('name', user['name'])
    
    if 'zodiac_sign' in request.form:
        if 'preferences' not in user:
            user['preferences'] = {}
        user['preferences']['zodiac_sign'] = request.form.get('zodiac_sign')
    
    db['users'][session['user_id']] = user
    
    flash('Profile updated successfully', 'success')
    return redirect(url_for('profile.profile'))
