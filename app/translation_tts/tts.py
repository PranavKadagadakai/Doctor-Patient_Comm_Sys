from gtts import gTTS
from googletrans import Translator
import os
import uuid

translator = Translator()

def text_to_speech(text, lang='en'):
    try:
        translated = translator.translate(text, dest=lang).text
        print(f"Translated text: {translated}")

        audio_dir = os.path.join('uploads/audio')
        os.makedirs(audio_dir, exist_ok=True)

        filename = f"{uuid.uuid4().hex}.mp3"
        path = os.path.join(audio_dir, filename)

        tts = gTTS(text=translated, lang=lang)
        tts.save(path)

        return path, translated
    except Exception as e:
        print(f"[TTS ERROR] {e}")
        raise e
