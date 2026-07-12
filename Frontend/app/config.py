import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = st.secrets.get("BASE_URL", os.getenv("BASE_URL", ""))
    GNEWS_API_KEY = st.secrets.get("GNEWS_API_KEY", os.getenv("GNEWS_API_KEY", ""))
