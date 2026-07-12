import streamlit as st
from src.utils.helpers import format_published_date, truncate_text
from typing import List, Dict

def render_news_feed(news_articles: List[Dict]):
    """Display a grid of news cards."""
    if not news_articles:
        st.info("No articles to display.")
        return

    st.markdown("## Latest News")
    
    # Two columns for responsive grid
    cols = st.columns(2)
    for idx, article in enumerate(news_articles):
        with cols[idx % 2]:
            render_news_card(article)

def render_news_card(article: Dict):
    """Single news card."""
    title = article.get("title", "Untitled")
    description = article.get("description", "")
    image = article.get("image")
    source = article.get("source", "Unknown")
    published = article.get("published_at", "")
    url = article.get("url", "#")

    # Truncate description
    if description:
        description = truncate_text(description, 120)
    
    # Format date
    date_str = format_published_date(published)

    card_html = f"""
    <div class="news-card">
        {f'<img class="card-image" src="{image}" alt="News image" />' if image else '<div class="card-image-placeholder">📰</div>'}
        <div class="card-body">
            <div class="card-meta">
                <span class="source">{source}</span>
                <span class="date">{date_str}</span>
            </div>
            <h3 class="card-title">{title}</h3>
            {f'<p class="card-description">{description}</p>' if description else ''}
            <a href="{url}" target="_blank" class="read-more">Read full article →</a>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)