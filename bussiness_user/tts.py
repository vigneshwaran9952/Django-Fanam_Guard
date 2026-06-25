# chatapp/tts.py
from gtts import gTTS
import io
import pypandoc
import re
# Use relative import to find vtt_utils inside the chatapp package
from . import vtt_utils 

def generate_speech(text, language_name, language_csv):
    """Generates audio bytes for the given text."""
    try:
        # Load language mapping from the utility module
        lang_map = vtt_utils.load_languages(language_csv)
        la_code = lang_map.get(language_name, "en")

        # Clean Markdown for better speech synthesis
        try:
            clean_text = pypandoc.convert_text(text, to='plain', format='md')
        except:
            # Fallback regex if pypandoc is not installed or fails
            clean_text = re.sub(r'[*#_~`>]', '', text)
        
        # Remove URLs/Hyperlinks from speech
        clean_text = re.sub(r'http\S+', '', clean_text).strip()

        if not clean_text:
            return None

        # Generate the Speech
        tts = gTTS(text=clean_text, lang=la_code, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Return the actual bytes for the Django JsonResponse
        return audio_buffer.getvalue() 
        
    except Exception as e:
        # Use standard print for server-side logging instead of st.error
        print(f"TTS Generation Error: {e}")
        return None