from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from .tts import text_to_speech
import os

translate_bp = Blueprint('translate', __name__)

@translate_bp.route('/translate_tts', methods=['POST'])
@jwt_required()
def translate_and_speak():
    print("Headers received:", dict(request.headers))
    current_user = get_jwt_identity()
    data = request.get_json()
    text = data.get('text')
    target_lang = data.get('target_lang')  # e.g. 'hi', 'fr', 'es'

    if not text or not target_lang:
        return jsonify({"error": "Missing text or target_lang"}), 400

    try:
        mp3_path, translated = text_to_speech(text, target_lang)
        filename = os.path.basename(mp3_path)

        return jsonify({
            "translated_text": translated,
            "audio_url": f"/api/translate_tts/audio/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@translate_bp.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    filepath = os.path.join('uploads/audio', filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath, mimetype='audio/mpeg')
