import requests
import streamlit as st
from config import Config

config = Config()
BASE_URL = config.BASE_URL

class ProfileAPI:
    def __init__(self, token):
        self.headers = {"Authorization": f"Bearer {token}"}

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
                except:
                    error_msg = response.text
                st.error(f"Request failed: {error_msg}")
                return None
            try:
                return response.json()
            except ValueError:
                st.error("Invalid JSON response")
                st.code(response.text)
                return None
        except Exception as e:
            st.error(f"Connection error: {e}")
            return None

    # ---- CRUD endpoints ----
    def get_profile(self):
        return self._request("GET", "/users/me")

    def update_profile(self, username=None, email=None):
        payload = {}
        if username:
            payload["username"] = username
        if email:
            payload["email"] = email
        return self._request("PUT", "/users/update", json=payload)

    def change_password(self, old_password, new_password):
        return self._request("PATCH", "/users/change-password", json={
            "old_password": old_password,
            "new_password": new_password
        })

    def delete_account(self):
        return self._request("DELETE", "/users/delete")
