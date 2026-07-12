import requests

from app.config.settings import settings


class HuggingFaceClient:

    BASE_URL = "https://router.huggingface.co/hf-inference/models"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.hf_token}",
            "Content-Type": "application/json"
        }

    def inference(self, model: str, payload: dict):
        """
        Generic inference method.

        model:
            facebook/bart-large-cnn
            deepset/roberta-base-squad2
            ...

        payload:
            {"inputs": "..."}
        """

        response = requests.post(
            f"{self.BASE_URL}/{model}",
            headers=self.headers,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()
