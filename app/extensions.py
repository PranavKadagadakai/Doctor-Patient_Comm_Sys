from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()
cors = CORS()

login_manager = LoginManager()
login_manager.login_view = 'main.login_page'  # redirects unauthorized users
