from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_jwt_extended import create_access_token
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash
from .decorators import login_required_ui
from app.chatbot.bot_engine import ChatBot

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

        # ✅ Store in session
        session['token'] = token
        session['role'] = user.role
        session['user_id'] = user.id

        return redirect(url_for('main.dashboard_page'))

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

@main_bp.route('/dashboard')
@login_required_ui
def dashboard_page():
    return render_template(
        'dashboard.html',
        role=session.get('role'),
        token=session.get('token')
    )

@main_bp.route('/logout')
@login_required_ui
def logout():
    session.clear()
    return redirect(url_for('main.home'))

@main_bp.route('/summarize')
@login_required_ui
def summarize_page():
    return render_template('summarize.html')

@main_bp.route('/chatbot')
@login_required_ui
def chatbot_page():
    return render_template('chatbot.html', token=session.get('token'))

@main_bp.route('/translate')
@login_required_ui
def translate_page():
    return render_template('translate.html')

@main_bp.route('/messaging')
@login_required_ui
def messaging_page():
    return render_template('messaging.html')

@main_bp.route('/forum')
@login_required_ui
def forum_page():
    return render_template('forum.html')

@main_bp.route('/tracker')
@login_required_ui
def tracker_page():
    return render_template('tracker.html')
