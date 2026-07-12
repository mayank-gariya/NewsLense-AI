# src/ui/sidebar.py
import streamlit as st

CATEGORIES = ["All", "Tech", "Sports", "Business", "World", "Science", "Health", "Entertainment"]

def render_sidebar():
    """Render the sidebar with category filter and search."""
    with st.sidebar:
        st.markdown("## 🔍 Filters")
        
        category = st.selectbox(
            "Category",
            options=CATEGORIES,
            index=0,
            key="sidebar_category"
        )
        
        search = st.text_input(
            "Search news",
            placeholder="Enter keyword...",
            key="sidebar_search"
        )
        
        st.markdown("---")
        st.markdown(
            """
            <div style="font-size:0.9rem;color:#888;">
                <p>💡 Tip: Search by topic, source, or event.</p>
                <p>📅 News updated every hour.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        return {"category": category, "search": search}