from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required
import io
from gtts import gTTS
from googletrans import Translator
import asyncio

translate_bp = Blueprint('translate', __name__)

@translate_bp.route('/translate', methods=['POST'])
def translate_tts():
    try:
        data = request.get_json()
        text = data['text']
        target_lang = data['target_lang']

        # Initialize the translator
        translator = Translator()

        # Run the async translation function
        translated = asyncio.run(translator.translate(text, dest=target_lang))

        # Generate TTS
        tts = gTTS(text=translated.text, lang=target_lang)
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)

        # Stream audio with correct headers
        return Response(
            audio_io,
            mimetype='audio/mpeg',
            headers={
                'Content-Disposition': 'inline; filename=translated_audio.mp3'
            }
        )

    except Exception as e:
        print("[TTS ERROR]", str(e))
        return jsonify({"error": str(e)}), 500
