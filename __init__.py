from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail
import os
from uuid import uuid4

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = str(uuid4())
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

jwt = JWTManager(app)

app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')

oauth = OAuth(app)

google_bp = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
    client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    userinfo_url='https://www.googleapis.com/oauth2/v1/userinfo',
    scope='email profile'
)

app.register_blueprint(google_bp, url_prefix='/login/google')

# app.config['FACEBOOK_OAUTH_CLIENT_ID'] = os.getenv('FACEBOOK_OAUTH_CLIENT_ID')
# app.config['FACEBOOK_OAUTH_CLIENT_SECRET'] = os.getenv('FACEBOOK_OAUTH_CLIENT_SECRET')

# facebook_bp = oauth.register(
#     name='facebook',
#     client_id=app.config['FACEBOOK_OAUTH_CLIENT_ID'],
#     client_secret=app.config['FACEBOOK_OAUTH_CLIENT_SECRET'],
#     authorize_url='https://graph.facebook.com/oauth/authorize',
#     access_token_url='https://graph.facebook.com/oauth/access_token',
#     userinfo_url='https://graph.facebook.com/me',
#     scope='email'
# )

# app.register_blueprint(facebook_bp, url_prefix='/login/facebook')

mail = Mail(app)

from app import routes, models
