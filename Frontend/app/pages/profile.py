import streamlit as st
from datetime import datetime
from pathlib import Path
from src.api.profile_api import ProfileAPI

st.set_page_config(
    page_title="NewsLens · Profile",
    page_icon="👤",
    layout="wide"
)
# -----------------------------
# CSS
# -----------------------------
def load_css():
    main_css = Path(__file__).parent.parent / "styles" / "custom.css"
    if main_css.exists():
        with open(main_css, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    profile_css = Path(__file__).parent.parent / "styles" / "profile.css"
    if profile_css.exists():
        with open(profile_css, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


# -----------------------------
# Authentication Check
# -----------------------------
if not st.session_state.get("token"):
    st.switch_page("Get_Started.py")


api = ProfileAPI(st.session_state["token"])

# -----------------------------
# Load User Profile Once
# -----------------------------
if st.session_state.get("user") is None:

    profile = api.get_profile()

    if profile:
        st.session_state["user"] = profile
    else:
        st.error("Unable to load profile.")
        st.stop()

profile = st.session_state["user"]


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.markdown("## 👤 User Menu")
    st.caption(f"Logged in as: {profile.get('username', 'User')}")

    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("Get_Started.py")


# -----------------------------
# Main Page
# -----------------------------
st.markdown('<div class="profile-card">', unsafe_allow_html=True)

st.header("Your Profile")

tabs = st.tabs(
    [
        "📋 View",
        "✏️ Update",
        "🔑 Change Password",
        "🗑️ Delete"
    ]
)

with tabs[0]:

    st.subheader("Profile Information")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="profile-field">
        <span class="label">Username</span>
        <span class="value">{profile.get("username","N/A")}</span>
        </div>

        <div class="profile-field">
        <span class="label">Email</span>
        <span class="value">{profile.get("email","N/A")}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="profile-field">
        <span class="label">Role</span>
        <span class="value">{profile.get("role","user")}</span>
        </div>

        <div class="profile-field">
        <span class="label">Joined</span>
        <span class="value">{profile.get("created_at","N/A")}</span>
        </div>
        """, unsafe_allow_html=True)


with tabs[1]:

    with st.form("update_form"):
        username = st.text_input(
            "Username",
            value=profile.get("username", "")
        )

        email = st.text_input(
            "Email",
            value=profile.get("email", "")
        )

        submitted = st.form_submit_button("Update Profile")

        if submitted:
            result = api.update_profile(username, email)

            if result:
                latest = api.get_profile()
                if latest:
                    st.session_state["user"] = latest

                st.success("Profile Updated")
                st.rerun()


with tabs[2]:

    with st.form("password_form"):

        old = st.text_input(
            "Current Password",
            type="password"
        )

        new = st.text_input(
            "New Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Change Password"
        )

        if submitted:
            if new != confirm:
                st.error("Passwords do not match.")

            elif len(new) < 6:
                st.error("Password should be at least 6 characters.")

            else:
                result = api.change_password(old, new)
                if result:
                    st.success("Password Changed")

with tabs[3]:

    st.warning(
        "This action cannot be undone."
    )

    with st.form("delete_form"):
        username = st.text_input(
            "Type your username"
        )

        submitted = st.form_submit_button(
            "Delete Account"
        )

        if submitted:
            if username != profile.get("username"):
                st.error("Username does not match.")

            else:
                result = api.delete_account()

                if result:
                    st.success("Account Deleted")
                    st.session_state.clear()
                    st.switch_page("Get_Started.py")


st.markdown("</div>", unsafe_allow_html=True)

st.caption(f"© {datetime.now().year} NewsLens")