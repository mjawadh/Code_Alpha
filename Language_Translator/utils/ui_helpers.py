"""
Reusable UI components for Streamlit.
"""

import streamlit as st

def render_header():
    st.title("🌍 Language Translator")
    st.markdown("A lightweight, offline-ready translation demo using mBART-large-50 (quantized 8-bit).")

def render_language_select(source_langs, target_langs):
    col1, col2 = st.columns(2)
    with col1:
        src = st.selectbox("Source Language", source_langs, index=0)
    with col2:
        tgt = st.selectbox("Target Language", target_langs, index=1)
    return src, tgt

def render_text_inputs():
    st.subheader("Enter text to translate:")
    return st.text_area("Input Text", height=150, placeholder="Type or paste text here...")

def render_tts_toggle():
    return st.toggle("Enable Text-to-Speech (optional)", value=False)

def render_result(translated_text):
    st.subheader("Translated Text:")
    st.success(translated_text)

def render_footer():
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit and mBART (quantized).")
