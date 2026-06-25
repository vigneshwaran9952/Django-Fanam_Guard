import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import pandas as pd
from deep_translator import GoogleTranslator

recognizer = sr.Recognizer()
LANGUAGE_CSV = "language_code.csv"


def load_languages(file_path=LANGUAGE_CSV):
    try:
        df = pd.read_csv(file_path)
        return pd.Series(df.Code.values, index=df.Language).to_dict()
    except Exception:
        return {"English": "en"}


def convert_audio_to_wav(uploaded_file):
    """
    Convert uploaded audio file to WAV (16kHz mono)
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        audio = AudioSegment.from_file(uploaded_file)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio.export(temp.name, format="wav")
        return temp.name


def audio_file_to_text(audio_file, user_language):
    """
    MAIN FUNCTION used by views.py
    """
    lang_map = load_languages()
    target_lang = lang_map.get(user_language, "en")

    wav_path = None
    try:
        wav_path = convert_audio_to_wav(audio_file)

        with sr.AudioFile(wav_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)

        # Always recognize in English
        english_text = recognizer.recognize_google(
            audio_data, language="en-US"
        )

        if user_language.lower() == "english":
            return english_text

        return GoogleTranslator(
            source="en", target=target_lang
        ).translate(english_text)

    except Exception as e:
        print("VTT ERROR:", e)
        return None

    finally:
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)
