from app import app
from flask import jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_jwt_extended import create_access_token
from flask_mail import Message
from app.models import User

@app.route('/')
def index():
    return jsonify(message='Welcome to the backend!')

@app.route('/register', methods=['POST'])
def register():
    # Implementation omitted for brevity
    pass

@app.route('/login', methods=['POST'])
def login():
    # Implementation omitted for brevity
    pass

@app.route('/logout')
@login_required
def logout():
    # Implementation omitted for brevity
    pass

@app.route('/profile')
@login_required
def profile():
    # Implementation omitted for brevity
    pass

@app.route('/password/recover', methods=['POST'])
def recover_password():
    # Implementation omitted for brevity
    pass

@app.route('/password/reset', methods=['POST'])
def reset_password():
    # Implementation omitted for brevity
    pass

@app.errorhandler(401)
def unauthorized(error):
    return jsonify(message='Unauthorized'), 401
