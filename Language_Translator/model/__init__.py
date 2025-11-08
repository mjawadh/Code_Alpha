"""
model package initializer.

Provides a stable import surface for the translation model.
Handles different possible translator implementations gracefully.
"""
from . import translator as _translator_mod

# Support both class-based Translator and function-based interfaces
Translator = getattr(_translator_mod, "Translator", None)
translate_text = getattr(_translator_mod, "translate_text", None)
load_model = getattr(_translator_mod, "load_model", None)
warmup_model = getattr(_translator_mod, "warmup_model", None)

# If the module exposes a single translate function under a different name, try common alternatives
if Translator is None and translate_text is None:
    translate_text = getattr(_translator_mod, "translate", None)

__all__ = ["Translator", "translate_text", "load_model", "warmup_model"]
