"""
translator.py
Handles model loading, quantization (8-bit), and translation logic.
Integrates with cache layer to prevent redundant processing.
"""

import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from cache.db_handler import fetch_cached_translation, store_translation
from config.settings import (
    MODEL_NAME,
    SUPPORTED_LANGUAGES,
    QUANTIZATION_BITS,
    MAX_INPUT_TOKENS,
    DEBUG_MODE
)

# =====================================================
# MODEL INITIALIZATION (Lazy Singleton)
# =====================================================


# Singleton model/tokenizer for efficiency
_model = None
_tokenizer = None


# =============================================
# Translator Class Wrapper
# =============================================
class Translator:
    def __init__(self, model_name=None, quantized=True):
        # model_name and quantized are accepted for compatibility, but config is global
        self.model, self.tokenizer = load_model()

    def translate(self, source_lang_name, target_lang_name, text):
        return translate_text(source_lang_name, target_lang_name, text)

    def warmup(self):
        warmup_model()


def load_model():
    """Load mBART model and tokenizer once, quantized to 8-bit."""
    global _model, _tokenizer

    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    if DEBUG_MODE:
        print("[MODEL INIT] Loading mBART-large-50...")

    # Load tokenizer
    _tokenizer = MBart50TokenizerFast.from_pretrained(MODEL_NAME)

    # Load model in quantized 8-bit form (CPU-friendly)
    model = MBartForConditionalGeneration.from_pretrained(MODEL_NAME)
    model = torch.quantization.quantize_dynamic(
        model, {torch.nn.Linear}, dtype=torch.qint8
    )

    model.eval()
    _model = model

    if DEBUG_MODE:
        print("[MODEL INIT] Model loaded and quantized.")
    return _model, _tokenizer


# =====================================================
# TRANSLATION CORE LOGIC
# =====================================================

def translate_text(source_lang_name: str, target_lang_name: str, text: str) -> str:
    """
    Main translation function.
    1. Checks cache.
    2. Tokenizes & translates.
    3. Saves result back to cache.
    """

    if not text.strip():
        return "⚠️ Empty input text."

    model, tokenizer = load_model()
    source_lang = SUPPORTED_LANGUAGES[source_lang_name]
    target_lang = SUPPORTED_LANGUAGES[target_lang_name]

    # Check cache first
    cached = fetch_cached_translation(source_lang, target_lang, text)
    if cached:
        if DEBUG_MODE:
            print("[CACHE HIT] Returning cached translation.")
        return cached

    # Tokenization & model inference
    tokenizer.src_lang = source_lang
    encoded = tokenizer(text, return_tensors="pt", truncation=True, max_length=MAX_INPUT_TOKENS)

    if DEBUG_MODE:
        print(f"[TRANSLATE] Tokens: {len(encoded['input_ids'][0])}")

    with torch.no_grad():
        generated_tokens = model.generate(
            **encoded,
            forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
            max_length=MAX_INPUT_TOKENS
        )

    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0].strip()

    # Save in cache
    store_translation(source_lang, target_lang, text, translated_text)

    if DEBUG_MODE:
        print("[TRANSLATE] Translation completed and cached.")

    return translated_text


# =====================================================
# PERFORMANCE HELPERS
# =====================================================

def warmup_model():
    """Run a dummy inference to pre-load weights (for first-run delay reduction)."""
    model, tokenizer = load_model()
    dummy_text = "Hello world."
    _ = translate_text("English", "Spanish", dummy_text)
    if DEBUG_MODE:
        print("[WARMUP] Model warmed up successfully.")
