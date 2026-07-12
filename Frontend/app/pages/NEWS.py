import streamlit as st
from src.ui.header import render_header
from src.ui.welcome import render_welcome
from src.ui.news_feed import render_news_feed
from src.ui.sidebar import render_sidebar
from src.api.gnews_client import GNewsClient

from config import Config
import logging
from pathlib import Path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Newslense.AI",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def load_custom_css():
    css_path = Path(__file__).parent.parent / "styles" / "custom.css"

    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )
    else:
        st.error(f"CSS file not found: {css_path}")

def main():
    load_custom_css()

    config = Config()
    news_client = GNewsClient(config.GNEWS_API_KEY)

    # Session state
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "All"
    if "news_data" not in st.session_state:
        st.session_state.news_data = []
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

    # Sidebar filters
    sidebar_filters = render_sidebar()
    if sidebar_filters:
        st.session_state.selected_category = sidebar_filters.get("category", "All")
        st.session_state.search_query = sidebar_filters.get("search", "")

    # Header with category tabs
    selected_category = render_header(
        st.session_state.selected_category,
        st.session_state.search_query
    )
    if selected_category:
        st.session_state.selected_category = selected_category

    # Map category to API parameter
    category_map = {
        "All": "general",
        "Tech": "technology",
        "Sports": "sports",
        "Business": "business",
        "World": "world",
        "Science": "science",
        "Health": "health",
        "Entertainment": "entertainment"
    }
    api_category = category_map.get(st.session_state.selected_category, "general")

    # Fetch news if needed
    if (not st.session_state.news_data or 
        st.session_state.get("last_category") != api_category or
        st.session_state.get("last_search") != st.session_state.search_query):
        with st.spinner("Fetching latest news..."):
            try:
                if st.session_state.search_query:
                    news_data = news_client.search_news(
                        st.session_state.search_query,
                        max_results=20
                    )
                else:
                    news_data = news_client.get_top_headlines(
                        category=api_category,
                        max_results=20
                    )
                st.session_state.news_data = news_data
                st.session_state.last_category = api_category
                st.session_state.last_search = st.session_state.search_query
            except Exception as e:
                st.error(f"Failed to fetch news: {str(e)}")
                st.session_state.news_data = []

    # Welcome banner (only on "All" with no search)
    if st.session_state.selected_category == "All" and not st.session_state.search_query:
        render_welcome()

    # News feed
    if st.session_state.news_data:
        render_news_feed(st.session_state.news_data)
    else:
        st.info("No articles found. Try adjusting your filters or search.")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 20px 0; font-size: 0.9rem;">
            <p>Built with ❤️ using Streamlit, NLP, and Hugging Face Transformers</p>
            <p>© 2026 Newslense.AI — Not another simple news app, powered by AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
