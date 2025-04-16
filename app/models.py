# app/models.py

from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    # One-to-one relationship
    profile = db.relationship('Profile', uselist=False, back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    full_name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    address = db.Column(db.String(200))
    usn = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='profile')  # <--- THIS was missing
