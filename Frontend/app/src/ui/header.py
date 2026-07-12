# src/ui/header.py
import streamlit as st

CATEGORIES = ["All", "Tech", "Sports", "Business", "World", "Science", "Health", "Entertainment"]

def render_header(selected_category: str, search_query: str) -> str:
    """Render the top navigation bar with categories."""
    st.markdown(
        """
        <div class="header-container">
            <div class="header-left">
                <span class="logo">📰 Newslense.AI</span>
                <span class="tagline">Smart news, simply delivered</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Category tabs
    cols = st.columns(len(CATEGORIES))
    for idx, cat in enumerate(CATEGORIES):
        with cols[idx]:
            if st.button(
                cat,
                key=f"tab_{cat}",
                use_container_width=True,
                type="primary" if cat == selected_category else "secondary"
            ):
                return cat

    return selected_category 