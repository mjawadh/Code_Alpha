"""
settings.py
Central configuration file for Translation App.
Defines constants, supported languages, quantization preferences,
and cache management settings.
"""

import os
from pathlib import Path

# =====================================================
# PATHS & DIRECTORIES
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
DB_PATH = CACHE_DIR / "translations.db"

os.makedirs(CACHE_DIR, exist_ok=True)

# =====================================================
# TRANSLATION MODEL CONFIGURATION
# =====================================================

# Model ID (mBART-large-50 supports 50 languages)
MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"

# Quantization setting — 8-bit for CPU efficiency
QUANTIZATION_BITS = 8

# Max input length before truncation/splitting
MAX_INPUT_TOKENS = 256

# =====================================================
# LANGUAGE CONFIGURATION
# =====================================================

# Limiting to seven widely used languages for performance and UI clarity
SUPPORTED_LANGUAGES = {
    "English": "en_XX",
    "Spanish": "es_XX",
    "French": "fr_XX",
    "German": "de_DE",
    "Chinese": "zh_CN",
    "Arabic": "ar_AR",
    "Hindi": "hi_IN"
}


LANGUAGES = ["English", "Spanish", "French", "German", "Chinese", "Arabic", "Hindi"]
MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"
MAX_TOKENS = 256



# Default source/target languages
DEFAULT_SOURCE = "English"
DEFAULT_TARGET = "Spanish"

# =====================================================
# CACHE SETTINGS
# =====================================================

CACHE_RETENTION_DAYS = 7     # Automatically clean records older than this
MAX_CACHE_ROWS = 1000        # Purge oldest if over limit
MAX_DB_SIZE_MB = 50          # Cleanup trigger on oversized DB

# =====================================================
# UI CONFIGURATION
# =====================================================

APP_TITLE = "Polyglot Translator 🌍"
APP_DESCRIPTION = (
    "An offline-first multilingual translation tool powered by mBART-large-50, "
    "supporting text translation and optional text-to-speech."
)

# Streamlit theme (you can override in .streamlit/config.toml)
UI_THEME = {
    "primaryColor": "#0078D7",
    "backgroundColor": "#0E1117",
    "secondaryBackgroundColor": "#262730",
    "textColor": "#FAFAFA",
    "font": "sans serif"
}

# =====================================================
# TTS SETTINGS
# =====================================================

# Available modes
TTS_MODES = {
    "None": None,
    "Offline (pyttsx3)": "offline",
    "Online (gTTS)": "online"
}

# Default mode
DEFAULT_TTS_MODE = "Offline (pyttsx3)"

# =====================================================
# PERFORMANCE SETTINGS
# =====================================================

# Set this to True for debugging (logs tokenization and translation timings)
DEBUG_MODE = False
