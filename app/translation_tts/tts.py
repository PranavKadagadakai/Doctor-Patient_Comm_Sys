from gtts import gTTS
import os
import uuid

def text_to_speech(text, lang='en'):
    audio_dir = os.path.join('uploads/audio')
    os.makedirs(audio_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.mp3"
    path = os.path.join(audio_dir, filename)

    tts = gTTS(text, lang=lang)
    tts.save(path)

    return path
