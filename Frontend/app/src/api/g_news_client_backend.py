import requests
import streamlit as st
from config import Config

config = Config()
BASE_URL = config.BASE_URL

class GNewsClient:
    def __init__(self, token=None):
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
            
    def _request(self, method, endpoint, **kwargs):
        try:
            response = requests.request(
                method,
                f"{BASE_URL}{endpoint}",
                headers=self.headers,
                **kwargs
            )

            if response.status_code != 200:
                try:
                    error_msg = response.json().get("detail", response.text)
                except Exception:
                    error_msg = response.text

                st.error(f"Request failed: {error_msg}")
                return None

            return response.json()

        except Exception as e:
            st.error(f"Connection error: {e}")
            return None

    # ---- News endpoints ----
    def get_news(self):
        """Fetch all news articles."""
        return self._request("GET", "/news/latest")

    # ---- AI endpoints ----
    def get_summary(self, article_id):
        """Generate summary for an article."""
        return self._request("GET", f"/news/summary/{article_id}")

    def get_qa(self, article_id, question):
        """Ask a question about the article."""
        return self._request("POST", f"/news/question-answer/{article_id}", json={"question": question})

    def get_sentiment(self, article_id):
        """Analyze sentiment of the article."""
        return self._request("GET", f"/news/sentiment/{article_id}")

    def get_topic(self, article_id):
        """Classify topic of the article."""
        return self._request("GET", f"/news/topic/{article_id}")
    
    def get_entities(self, article_id):
        return self._request(
            "GET",
            f"/news/entities/{article_id}"
        )

    def get_keywords(self, article_id):
        return self._request(
            "GET",
            f"/news/keywords/{article_id}"
        )

    # ---- Admin ----
    def refresh_news(self):
        """Trigger news refresh (admin only)."""
        return self._request("POST", "/news/refresh")