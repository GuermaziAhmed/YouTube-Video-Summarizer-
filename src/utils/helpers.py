from gtts import gTTS
from io import BytesIO

def generate_tts(summary, language_code):
    try:
        tts = gTTS(summary, lang=language_code)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        return mp3_fp
    except Exception as e:
        return None