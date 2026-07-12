import streamlit as st
from src.utils.helpers import format_published_date, truncate_text

def display_news_card(article, on_ai_click, on_read_click):
    """
    Display a single news card inside the given column.
    article: dict with keys: id, title, description, content, url, image, source, published_at
    on_ai_click: callback function expecting article
    on_read_click: callback function expecting article
    """
    with st.container():
        
        image_url = article.get("image")
        if image_url:
            st.image(image_url, use_column_width=True)
        else:
            st.markdown('<div class="card-image-placeholder">📰</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card-meta">
            <span class="source">{article.get('source', 'Unknown')}</span>
            <span class="date">{format_published_date(article.get('published_at'))}</span>
        </div>
        """, unsafe_allow_html=True)

        # Title
        st.markdown(f"<h3 class='card-title'>{article.get('title', 'Untitled')}</h3>", unsafe_allow_html=True)

        # Description
        desc = truncate_text(article.get("description", ""), 120)
        st.markdown(f"<p class='card-description'>{desc}</p>", unsafe_allow_html=True)

        # Action buttons
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.button(
                "📖 Read Full Article",
                key=f"read_{article['id']}",
                on_click=on_read_click,
                args=(article,)
            )
        with col2:
            st.button(
                "✨ AI Assistant",
                key=f"ai_{article['id']}",
                on_click=on_ai_click,
                args=(article,)
            )
        with col3:
            st.button(
                "☆",
                key=f"bookmark_{article['id']}",
                help="Bookmark (coming soon)"
            )