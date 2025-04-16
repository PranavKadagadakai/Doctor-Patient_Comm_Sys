from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt, socketio, cors
from .auth.routes import auth_bp
from .summarization.routes import summarization_bp
from .chatbot.routes import chatbot_bp
from .messaging import events  # register socket events
from .translation_tts.routes import translate_bp
from .forum.routes import forum_bp
from .tracker.routes import tracker_bp
from .main.routes import main_bp
from .profile.routes import profile_bp
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from .extensions import login_manager
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": ["http://localhost:5000"]}},
              supports_credentials=True,
              expose_headers=["Authorization"])
        
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(summarization_bp, url_prefix='/api/summarization')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(translate_bp, url_prefix='/api/translate_tts')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')
    app.register_blueprint(tracker_bp, url_prefix='/api/tracker')
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp)

    # @app.context_processor
    # def inject_user():
    #     return {
    #         'role': session.get('role'),
    #         'token': session.get('token')
    #     }
    # @app.context_processor
    # def inject_profile():
    #     if current_user.is_authenticated:
    #         return dict(user=current_user, profile=current_user.profile)
    #     return dict(user=None, profile=None)

    
    return app
