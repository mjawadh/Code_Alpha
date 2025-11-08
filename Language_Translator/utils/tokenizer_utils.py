"""
Text preprocessing helpers for the translation app.
Handles normalization, stripping, and safe token truncation.
"""

import re

def clean_text(text: str) -> str:
    """Basic text cleanup: remove extra whitespace, weird symbols."""
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[“”‘’]", '"', text)
    return text

def truncate_text(text: str, max_tokens: int = 256) -> str:
    """
    Rough token limiter to avoid overfeeding the model on CPU.
    We're not using tokenizer here because it's overkill for cleaning.
    """
    words = text.split()
    if len(words) > max_tokens:
        words = words[:max_tokens]
    return " ".join(words)
