from app.clients.huggingface_client import HuggingFaceClient


class SentimentInference:

    def __init__(self):
        self.client = HuggingFaceClient()
        self.model = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    def analyze(self, text: str):

        if not text:
            return {
                "label": "NEUTRAL",
                "score": 0
            }

        # limit long articles
        text = text[:1000]

        result = self.client.inference(
            self.model,
               {
                "inputs": text,
                "parameters": {
                    "truncation": True
                }
            }
        )

        while isinstance(result, list):
            if not result:
                return {
                    "label": "UNKNOWN",
                    "score": 0
                }
            result = result[0]

        return {
            "label": result.get("label", "UNKNOWN"),
            "score": round(result.get("score", 0), 4)
        }
