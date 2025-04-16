from flask import Blueprint, request, jsonify
from ..models import User
from ..extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'User already exists'}), 400

    user = User(email=data['email'], role=data['role'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Registration successful'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify(access_token=access_token)

