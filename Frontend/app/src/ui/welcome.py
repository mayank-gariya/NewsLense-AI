# src/ui/welcome.py
import streamlit as st

def render_welcome():
    """Display the welcome section with project info and tech stack."""
    st.markdown(
        """
        <div class="welcome-banner">
            <h1>👋 Welcome to Newslense.AI</h1>
            <p class="subtitle">Built by <strong>Mayank Gariya</strong> — not another simple news app, 
            but a smart, AI‑powered experience.</p>
            <div class="tech-stack">
                <span class="tech-badge">🧠 NLP</span>
                <span class="tech-badge">🤗 Hugging Face Transformers</span>
                <span class="tech-badge">📚 Transfer Learning</span>
                <span class="tech-badge">🔍 spaCy</span>
                <span class="tech-badge">⚡ YAKE</span>
                <span class="tech-badge">📊 Streamlit</span>
                <span class="tech-badge">🌐 GNews API</span>
            </div>
            <p class="description">Discover a world of news that matters to you, curated with intelligence 
            and designed for clarity.</p>
        </div>
        """,
        unsafe_allow_html=True
    )