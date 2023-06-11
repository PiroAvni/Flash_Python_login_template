from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin

from app import app,db

app.app_context().push()
db.create_all()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
 
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.name}>'
    
with app.app_context():
    db.create_all()
    print("Database tables created")    