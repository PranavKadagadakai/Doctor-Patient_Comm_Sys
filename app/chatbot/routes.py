from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .bot_engine import bot

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
# @jwt_required()
def chat():
    print("=== HEADERS ===")
    print(request.headers)

    print("=== RAW BODY ===")
    print(request.get_data(as_text=True))  # See raw incoming body

    print("=== PARSED JSON ===")
    data = request.get_json(silent=True)
    print(data)

    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400

    user_input = data['message']
    print("=== USER INPUT ===")
    print(user_input, type(user_input))
    try:
        response = bot.get_response(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500