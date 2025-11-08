import streamlit as st
from model.translator import Translator
from cache.db_handler import CacheDBHandler
from config import settings
from utils.tokenizer_utils import clean_text, truncate_text
from utils.ui_helpers import (
    render_header,
    render_language_select,
    render_text_inputs,
    render_result,
    render_tts_toggle,
    render_footer,
)
import pyttsx3
import os


# -------------------------
# App Initialization
# -------------------------
st.set_page_config(
    page_title="Language Translator",
    layout="centered",
    page_icon="🌍",
)

render_header()

# Load available languages
SOURCE_LANGS = settings.LANGUAGES
TARGET_LANGS = settings.LANGUAGES

# Initialize model (lazy load)
@st.cache_resource(show_spinner=True)
def load_translator():
    return Translator(model_name=settings.MODEL_NAME, quantized=True)

translator = load_translator()

# Initialize Cache
db_path = os.path.join("cache", "translations.db")
cache_handler = CacheDBHandler(db_path=db_path)
cache_handler.create_tables()


# -------------------------
# UI Logic
# -------------------------
src_lang, tgt_lang = render_language_select(SOURCE_LANGS, TARGET_LANGS)
input_text = render_text_inputs()
enable_tts = render_tts_toggle()

if st.button("Translate"):
    cleaned_text = clean_text(input_text)
    truncated_text = truncate_text(cleaned_text, max_tokens=settings.MAX_TOKENS)

    if not truncated_text:
        st.warning("Please enter text to translate.")
    else:
        # Step 1: Check Cache
        cached = cache_handler.get_cached_translation(src_lang, tgt_lang, truncated_text)
        if cached:
            st.info("Loaded from cache ✅")
            translated_text = cached
        else:
            # Step 2: Perform Translation
            with st.spinner("Translating... please wait"):
                translated_text = translator.translate(src_lang, tgt_lang, truncated_text)
                cache_handler.add_translation(truncated_text, translated_text, src_lang, tgt_lang)

        # Step 3: Display Result
        render_result(translated_text)

        # Step 4: Optional TTS
        if enable_tts:
            try:
                engine = pyttsx3.init()
                engine.say(translated_text)
                engine.runAndWait()
            except Exception:
                st.warning("TTS unavailable for this language or system voice settings.")



