from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.controllers.User import register, login, logout, recover_password, reset_password, get_all_users,update_user_profile, get_user_profile
from flask_cors import CORS

user_bp = Blueprint('user', __name__)

CORS(user_bp)

# @user_bp.route('/')
# def index():
#     return 'Hello, World!'

@user_bp.route('/users', methods=['GET'])
def get_all_users_route():
    return get_all_users()

@user_bp.route('/register', methods=['POST'])
def register_route():
    return register()

@user_bp.route('/login', methods=['GET','POST'])
def login_route():
    return login()

@user_bp.route('/logout', methods=['POST'])
@login_required
def logout_route():
    return logout()


@user_bp.route('/profile', methods=['GET'])
@login_required
def profile_route():
    return get_user_profile()

@user_bp.route('/profile', methods=['POST'])
@login_required
def update_profile_route():
    return update_user_profile()


# @user_bp.route('/password/recover', methods=['POST'])
# def recover_password_route():
#     return recover_password()

# @user_bp.route('/password/reset', methods=['POST'])
# def reset_password_route():
#     return reset_password()

@user_bp.errorhandler(401)
def unauthorized(error):
    return jsonify(message='Unauthorized'), 401

@user_bp.route('/', methods=['POST'])
def handle_post_request():
    # Get the data from the request body
    data = request.get_json()

    # Perform some processing with the data
    # Replace this with your actual logic
    processed_data = process_data(data)

    # Return a response
    return jsonify(result=processed_data)