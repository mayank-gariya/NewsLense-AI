import streamlit as st

def render_sidebar(profile, client):
    """Render the styled sidebar with user info, logout, and admin controls."""
    with st.sidebar:
        # --- Profile Card ---
        st.markdown(f"""
        <div style="
            border-radius: 16px;
            padding: 1rem 1.25rem;
            box-shadow: 0 4px 12px rgba(108, 60, 225, 0.08);
            border: 1px solid #f0ecff;
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                <span style="font-size: 2rem;">👤</span>
                <span style="font-weight: 700; color: white ; font-size: 1.1rem;">User</span>
            </div>
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 0.25rem 0.75rem; font-size: 0.9rem;">
                <span style="color: white; font-weight: 500;">Username</span>
                <span style="color: white; font-weight: 500;">{profile.get('username', '')}</span>
                <span style="color: white; font-weight: 500;">Email</span>
                <span style="color: white; font-weight: 500;">{profile.get('email', '')}</span>
                <span style="color: white; font-weight: 500;">Role</span>
                <span style="color: white; font-weight: 500;">{profile.get('role', '')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- Logout Button ---
        if st.button("Logout", key="logout_sidebar"):
            st.session_state.clear()
            st.switch_page("Get_Started.py")

        # --- Admin Section ---
        if profile.get("role") == "admin":
            st.markdown("""
            <div style="margin: 1rem 0 0.5rem 0; border-top: 1px solid #ede7ff;"></div>
            <div style="font-weight: 600; color:white; font-size: 1rem; margin-bottom: 0.5rem;">
                🛠️ Admin
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔄 Refresh News", key="refresh_news_sidebar"):
                with st.spinner("Refreshing database..."):
                    result = client.refresh_news()
                    if result:
                        st.success("Database refreshed")
                        st.rerun()
                    else:
                        st.error("Refresh failed")