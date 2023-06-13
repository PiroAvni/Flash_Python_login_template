from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from uuid import uuid4
from flask import Blueprint,  url_for, redirect
from authlib.integrations.flask_client import OAuth

user_bp = Blueprint('user', __name__)


app = Flask(__name__)
CORS(app)

oauth = OAuth()
app.config['SECRET_KEY'] = str(uuid4())
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://wzbnizjp:t0hJ4zOrnOHFn3OlV3dRMIUSq6yp5B8O@mel.db.elephantsql.com/wzbnizjp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user.login_route'
jwt = JWTManager(app)
mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    from app.models.User import User
    return User.query.get(int(user_id))

# Configure JWT to store tokens in cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Set to True for production, if using HTTPS
app.config['JWT_COOKIE_CSRF_PROTECT'] = True  # Enable CSRF protection for cookies

with app.app_context():
    db.create_all()

# Import and register the blueprints
from app.routes.User import user_bp
app.register_blueprint(user_bp)






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
