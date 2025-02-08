
from deep_translator import GoogleTranslator

def translate_text(text: str, target_language: str) -> str:
    try:
        translation = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translation
    except Exception as e:
        return f"Error: {str(e)}"
