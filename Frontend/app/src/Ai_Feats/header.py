import streamlit as st

def render_header(title="NewsLens", subtitle="AI-powered news at your fingertips"):
    st.markdown(f"""
    <div class="header-container">
        <div class="header-left">
            <span class="logo">📰 {title}</span>
            <span class="tagline">{subtitle}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)