from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_jwt_extended import create_access_token
from app.models import User, Profile
from app.extensions import db
# from werkzeug.security import generate_password_hash
# from .decorators import login_required_ui
from flask_login import login_user, logout_user, login_required, current_user


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('landing.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return "Invalid credentials", 401

        login_user(user)  # This is the key part

        return redirect(url_for('main.dashboard_page'))

    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # passed from form
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        usn = request.form.get('usn')

        # check if user exists
        if User.query.filter_by(email=email).first():
            return "User already exists", 400

        user = User(email=email, username=username)
        user.set_password(password)

        profile = Profile(
            role=role,
            full_name=full_name,
            phone=phone,
            address=address,
            usn=usn,
        )

        user.profile = profile

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.login_page'))

    return render_template('register.html')

@main_bp.route('/dashboard')
@login_required
def dashboard_page():
    user = current_user
    profile = Profile.query.filter_by(user_id=user.id).first()  # ✅ Add .first()

    role = profile.role if profile else "Unknown"

    return render_template(
        'dashboard.html',
        role=role,
        username=user.username
    )

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.home'))


@main_bp.route('/summarize')
@login_required
def summarize_page():
    return render_template('summarize.html', token=session.get('token'))

@main_bp.route('/chatbot')
@login_required
def chatbot_page():
    return render_template('chatbot.html', token=session.get('token'))

@main_bp.route('/translate')
@login_required
def translate_page():
    return render_template('translate.html', token=session.get('token'))

@main_bp.route('/messaging')
@login_required  # Changed from login_required_ui to login_required
def messaging_page():
    user = current_user
    profile = Profile.query.filter_by(user_id=user.id).first()  # ✅ Add .first()

    role = profile.role if profile else "Unknown"
    
    # Check the role and render the appropriate template
    if role == 'doctor':
        return render_template('doctor_messaging.html', token=session.get('token'))
    elif role == 'patient':
        return render_template('patient_messaging.html', token=session.get('token'))
    else :
        return render_template('patient_messaging.html', token=session.get('token'))

@main_bp.route('/forum')
@login_required
def forum_page():
    return render_template('forum.html')

@main_bp.route('/contact')
def contact_page():
    return render_template('contact.html')

@main_bp.route('/about')
def about_page():
    return render_template('about.html')

@main_bp.route('/tracker')
@login_required
def tracker_page():
    return render_template('tracker.html')
