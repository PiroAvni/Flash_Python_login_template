from flask import Blueprint, jsonify, request, make_response
from flask_login import login_required
from app.controllers.User import register, login, logout, recover_password, reset_password, get_all_users, update_user_profile, get_user_profile
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)
CORS(user_bp)


@user_bp.route('/')
def index():
    return 'Hello, World!'


@user_bp.route('/users', methods=['GET'])
def get_all_users_route():
    return jsonify(get_all_users())


@user_bp.route('/register', methods=['POST'])
def register_route():
    return register()


@user_bp.route('/login', methods=['GET','POST'])
def login_route():
    response, status_code = login()
    return set_cookie(response, 'access_token', response.json.get('access_token'))


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout_route():
    response = logout()
    return unset_cookie(response, 'access_token')


@user_bp.route('/profile', methods=['GET'])
@login_required
def profile_route():
    return get_user_profile()


@user_bp.route('/profile', methods=['POST'])
@login_required
def update_profile_route():
    return update_user_profile()


@user_bp.errorhandler(401)
def unauthorized(error):
    return jsonify(message='Unauthorized'), 401


@user_bp.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': 'Protected route', 'user': current_user}), 200


def set_cookie(response, name, value):
    response.set_cookie(name, value=value, httponly=True)
    return response


def unset_cookie(response, name):
    response = make_response(response)  # Convert the tuple response to a Response object
    response.delete_cookie(name)
    return response

# @user_bp.route('/', methods=['POST'])
# def handle_post_request():
#     # Get the data from the request body
#     data = request.get_json()

#     # Perform some processing with the data
#     # Replace this with your actual logic
#     processed_data = process_data(data)

#     # Return a response
#     return jsonify(result=processed_data)