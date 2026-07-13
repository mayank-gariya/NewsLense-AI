import streamlit as st
import requests
from config import Config
from datetime import datetime
from pathlib import Path

backend_url = "https://backend-q23l.onrender.com"
current_year = datetime.now().year

st.set_page_config(page_title="NewsLens · Auth", page_icon="🔐", layout="centered")

def load_css():
    css_path = Path(__file__).parent / "styles" / "login.css"
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

config = Config()

defaults = {
    "token": None,
    "profile": None,
    "username": None,
    "email": None,
    "role": None,
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)
    
url = config.BASE_URL

if st.session_state.get("token"):
    st.switch_page("pages/Ai_Features.py")
    
# ---- AUTH UI ----
st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="auth-box">', unsafe_allow_html=True)
st.markdown('<div class="auth-header">📰 NewsLens</div>', unsafe_allow_html=True)
st.markdown('<p class="auth-subtitle">Sign in to access AI-powered insights</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Create Account", "Log In"])

with tab1:
    with st.form("register_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Min 6 characters")
        submitted = st.form_submit_button("Register", use_container_width=True)
        if submitted:
            if not username or not email or not password:
                st.error("All fields are required.")
            else:
                response = requests.post(
                    f"{url}/auth/register",
                    json={"username": username, "email": email, "password": password},
                )
                if response.status_code == 200:
                    st.success("✅ Registration successful! You can now log in.")
                else:
                    st.error(f"❌ Registration failed: {response.text}")
                with st.expander("📦 API Response"):
                    st.json(response.json())

with tab2:
    with st.form("login_form"):

        email = st.text_input(
            "Email",
            placeholder="your@email.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        submitted = st.form_submit_button(
            "Log In",
            use_container_width=True
        )

        if submitted:

            if not email or not password:
                st.error("Please fill in all fields.")

            else:
                response = requests.post(
                    f"{url}/auth/login",
                    json={
                        "email": email,
                        "password": password
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    token = data["access_token"]
                    st.session_state["token"] = token

                    # ----------------------------
                    # Fetch logged in user
                    # ----------------------------

                    profile_response = requests.get(
                        f"{url}/users/me",
                        headers={
                            "Authorization": f"Bearer {token}"
                        }
                    )
                    
                    if profile_response.status_code == 200:
                        profile = profile_response.json()

                        st.session_state["profile"] = profile
                        st.session_state["username"] = profile.get("username")
                        st.session_state["email"] = profile.get("email")
                        st.session_state["role"] = profile.get("role")
                        
                        st.success("Login Successful")
                        st.switch_page("pages/Ai_Features.py")

                    else:
                        st.error("Unable to load user profile.")
                else:
                    try:
                        st.error(response.json()["detail"])
                    except Exception:
                        st.error("Login Failed")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown(
    f"<p style='color: #6c757d; font-size: 0.8rem;'>© {current_year} NewsLens and make sure you wakeup 😴 the <a href='{backend_url}' target='_blank' style='color: #6c757d; text-decoration: underline;'>backend</a></p>",
    unsafe_allow_html=True,
)
