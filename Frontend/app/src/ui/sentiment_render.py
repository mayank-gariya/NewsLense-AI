import streamlit as st

def render_sentiment(sentiment_data: dict):
    """
    Display sentiment label and confidence in a purple‑themed card.
    Expects a dict with keys: 'label' (string) and 'score' (float, 0-1).
    """
    if not sentiment_data:
        return

    label = sentiment_data.get("label", "Neutral")
    score = sentiment_data.get("score", 0.0)

    # Emoji/icon based on sentiment
    icon_map = {
        "positive": "😊",
        "neutral": "😐",
        "negative": "😟",
    }
    
    icon = icon_map.get(label.lower(), "🔍")

    # Color mapping for sentiment
    color_map = {
        "positive": "#059669",   # green
        "neutral": "#6b7280",    # gray
        "negative": "#dc2626",   # red
    }
    
    color = color_map.get(label.lower(), "#6b1cf4")  # fallback purple

    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h3 style="color: #6a0ffe; font-weight: 600;">🧠 Analyze Sentiment</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 12px rgba(108, 60, 225, 0.08);
        border: 1px solid #f0ecff;
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    ">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span style="font-size: 1.75rem;">{icon}</span>
            <div>
                <div style="font-size: 0.8rem; color: #7c6b9e; text-transform: uppercase; letter-spacing: 0.5px;">Sentiment</div>
                <div style="font-size: 1.25rem; font-weight: 600; color: {color};">{label.title()}</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="text-align: right;">
                <div style="font-size: 0.8rem; color: #7c6b9e; text-transform: uppercase; letter-spacing: 0.5px;">Confidence</div>
                <div style="font-size: 1.25rem; font-weight: 600; color: #2d1b69;">{score:.2f}</div>
            </div>
            <div style="width: 80px; height: 6px; background: #ede7ff; border-radius: 10px; overflow: hidden;">
                <div style="width: {score*100:.0f}%; height: 100%; background: #7c3aed; border-radius: 10px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)