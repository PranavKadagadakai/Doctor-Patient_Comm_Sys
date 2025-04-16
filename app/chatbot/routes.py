from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .bot_engine import bot

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400

    user_input = data['message']
    try:
        response = bot.get_response(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
