from googletrans import Translator
import os
import uuid
import asyncio
 
translator = Translator()
 
def text_to_speech(text, lang='en'):
    try:
        translated = asyncio.run(Translator.translate(text, lang))
        tts = gTTS(translated.text, lang=lang)
        path = f"static/audio/{lang}_output.mp3"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tts.save(path)
 
        return path, translated
    except:
        print("Error")