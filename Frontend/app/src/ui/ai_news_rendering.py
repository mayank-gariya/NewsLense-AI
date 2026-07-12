import streamlit as st
from datetime import datetime
from pathlib import Path
import html
import re


def load_css():
    """Load external CSS file or fallback inline CSS."""
    css_path = Path(__file__).parent.parent / "styles" / "ai_news_cards_style.css"

    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .article-card {
                background: #000000;
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 8px 30px rgba(108,60,225,0.12);
                margin-bottom: 1.5rem;
                transition: transform 0.2s;
            }
            .article-card:hover {
                transform: translateY(-4px);
            }
            .card-image {
                width: 100%;
                border-radius: 12px;
                margin-bottom: 1rem;
            }
            .card-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: #ffffff;
                margin: 0.5rem 0;
                line-height: 1.4;
            }
            .card-meta {
                font-size: 0.85rem;
                color: #b0b0b0;
                margin-bottom: 0.75rem;
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem 1rem;
            }
            .card-description {
                color: #ffffff;
                line-height: 1.6;
                margin-bottom: 0.5rem;
                font-size: 0.95rem;
            }
            .card-content-preview {
                color: #ffffff;
                line-height: 1.6;
                font-size: 0.95rem;
            }
            .read-more-link {
                color: #a78bfa;
                font-weight: 600;
                text-decoration: none;
                cursor: pointer;
            }
            .read-more-link:hover {
                color: #c4b5fd;
                text-decoration: underline;
            }
        </style>
        """, unsafe_allow_html=True)


def clean_text(text: str) -> str:
    """Remove HTML tags and stray HTML remnants."""
    if not text:
        return ""
    # Remove all HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Unescape HTML entities
    text = html.unescape(text)
    return text.strip()


def truncate_words(text: str, limit: int = 50):
    words = text.split()
    if len(words) <= limit:
        return text, "", False
    return " ".join(words[:limit]), " ".join(words[limit:]), True


def escape_text(text: str) -> str:
    """Escape HTML and convert newlines to <br>."""
    return html.escape(text).replace("\n", "<br>")


def render_card(article: dict):
    # --- Extract and clean all text fields ---
    title = escape_text(article.get("title", "Untitled"))
    description = escape_text(article.get("description", ""))

    raw_content = article.get("content") or ""
    cleaned_content = clean_text(raw_content)

    first_50, rest_content, is_truncated = truncate_words(cleaned_content, 50)

    # Escape the truncated parts
    first_50_escaped = escape_text(first_50)
    rest_content_escaped = escape_text(rest_content)

    # --- Meta fields ---
    source = escape_text(article.get("source", "Unknown Source"))
    url = article.get("url", "#")
    image = article.get("image", "")

    # Date formatting
    published = article.get("published_at", "")
    date_str = ""
    if published:
        try:
            dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
            date_str = dt.strftime("%b %d, %Y")
        except Exception:
            date_str = published

    # --- Build card HTML ---
    card_html = f"""
    <div class="article-card">
        {f'<img src="{image}" class="card-image" alt="{title}" />' if image else ''}
        <div class="card-title">{title}</div>
        <div class="card-meta">
            <span>🕒 {source}</span>
            {f'<span style="margin-left:1rem;">📅 {date_str}</span>' if date_str else ''}
        </div>
        {f'<div class="card-description">{description}</div>' if description else ''}
        <div class="card-content-preview">
            {first_50_escaped}
            {f'<span style="color:#7c3aed; font-weight:500;">…</span>' if is_truncated else ''}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # --- Expander for full content ---
    if is_truncated:
        with st.expander("📖 Show full content"):
            st.markdown(
                f"""
                <div style="background:#1a1a1a; padding:1rem; border-radius:10px;
                            color:#ffffff; line-height:1.7; font-size:0.95rem;">
                    {rest_content_escaped}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --- Read full article link ---
    if url and url != "#":
        st.markdown(
            f"""
            <div style="margin-top:0.75rem;">
                <a href="{url}" target="_blank" class="read-more-link">
                    🔗 Read full article →
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )



def ai_news(response):
    """Render all news cards in a 2‑column grid."""
    load_css()

    cols = st.columns(2)
    for i, article in enumerate(response):
        with cols[i % 2]:
            render_card(article)