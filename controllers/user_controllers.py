from app import app
from flask import jsonify, request, flask
from flask_login import login_user, logout_user, current_user, login_required
from flask_jwt_extended import create_access_token
from flask_mail import Message
from app.models import User

@app.route('/')
def index():
    return jsonify(message='Welcome to the backend!')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify(message='Username, email, and password are required'), 400
        
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            # Create a new user instance
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            
    return jsonify(message='User registered successfully'), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify(message='Email and password are required'), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return jsonify(message='Invalid email or password'), 401

    # Login the user
    login_user(user)
    
    # Generate an access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify(access_token=access_token), 200

@app.route('/logout')
@login_required
def logout():
    # Logout the user
    logout_user()
    
    return jsonify(message='User logged out successfully'), 200

@app.route('/profile')
@login_required
def profile():
    return jsonify(username=current_user.username, email=current_user.email)

@app.route('/password/recover', methods=['POST'])
def recover_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify(message='Email is required'), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(message='No user with that email exists'), 400

    # Generate a password recovery token
    token = user.generate_password_recovery_token()
    
    # Send password recovery email
    # Implementation omitted for brevity
    
    return jsonify(message='Password recovery email sent'), 200

@app.route('/password/reset', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')
    new_password = data.get('new_password')

    if not email or not token or not new_password:
        return jsonify(message='Email, token, and new password are required'), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password_recovery_token(token):
        return jsonify(message='Invalid email or token'), 401

    # Reset the user's password
    user.reset_password(new_password)
    
    return jsonify(message='Password reset successful'), 200

@app.errorhandler(401)
def unauthorized(error):
    return jsonify(message='Unauthorized'), 401
