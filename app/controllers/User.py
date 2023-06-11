from app import db
from flask import jsonify, request
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.models.User import User


bcrypt = Bcrypt()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_all_users():
    users = User.query.all()
    user_list = []

    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
            # Add other user attributes as needed
        }
        user_list.append(user_data)

    return user_list


def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return jsonify(message='name, email, and password are required'), 400

        email_exists = User.query.filter_by(email=email).first()
        name_exists = User.query.filter_by(name=name).first()
        if email_exists:
            return jsonify(message='Email is already in use.'), 400
        elif name_exists:
            return jsonify(message='name is already in use.'), 400
        elif len(name) < 2:
            return jsonify(message='name is too short.'), 400
        elif len(password) < 6:
            return jsonify(message='Password is too short.'), 400
        elif len(email) < 4:
            return jsonify(message='Email is invalid.'), 400
        else:

            # Hash the password
            hashed_password = bcrypt.generate_password_hash(
                password).decode('utf-8')

            # Create a new user instance
            new_user = User(name=name, email=email, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return jsonify(message='User created!'), 201

    return jsonify(message='User registered successfully'), 201


def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify(message='Email and password are required'), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify(message='Invalid email or password'), 401

    # Login the user
    login_user(user)

    # Generate an access token
    access_token = create_access_token(identity=user.id)

    return jsonify(access_token=access_token, email=user.email, name=user.name), 200


@login_required
def logout():
    # Logout the user
    logout_user()
    return jsonify(message='User logged out successfully'), 200


@login_required
def get_user_profile():

    # Assuming the user ID is passed in the request headers
    user_id = request.headers.get('user_id')
    # Fetch user from the database based on the user ID
    user = User.query.filter_by(id=user_id).first()
    print(user)

    if user:
        return jsonify({
            '_id': user.id,
            'name': user.name,
            'email': user.email
        })
    else:
        return jsonify(error='User not found'), 404


def update_user_profile():
    
    # Assuming the user ID is passed in the request headers
    user_id = request.headers.get('user_id')
    # Fetch user from the database based on the user ID
    user = User.query.filter_by(id=user_id).first()

    if user:
        user.name = request.json.get('name', user.name)
        user.email = request.json.get('email', user.email)

        password = request.json.get('password')
        if password:
            user.password = password

        db.session.commit()

        return jsonify({
            '_id': user.id,
            'name': user.name,
            'email': user.email
        })
    else:
        return jsonify(error='User not found'), 404

# @login_required
# def profile():
#     return jsonify(name=current_user.name, email=current_user.email)


# @login_required
# def update_profile():
#     data = request.get_json()
#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')

#     if not name or not email or not password:
#         return jsonify(message='name, email, and password are required'), 400

#     user = User.query.get(current_user.id)

#     # Update the name and email
#     user.name = name
#     user.email = email

#     # Update the password if provided
#     if password:
#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         user.password = hashed_password

#     db.session.commit()

#     return jsonify(message='Profile updated successfully'), 200


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

    return jsonify(message='Password recovery email sent'), 200


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
