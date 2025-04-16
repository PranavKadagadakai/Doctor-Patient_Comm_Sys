from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import create_access_token
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('landing.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return "Invalid credentials", 401

        token = create_access_token(identity={'id': user.id, 'role': user.role})
        return render_template('dashboard.html', token=token, role=user.role)

    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(email=email).first():
            return "User already exists", 400

        user = User(email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login_page'))

    return render_template('register.html')
