from app.clients.huggingface_client import HuggingFaceClient


class TopicClassifier:

    def __init__(self):
        self.client = HuggingFaceClient()
        self.model = "facebook/bart-large-mnli"

        self.labels = [
            "Politics",
            "Business",
            "Technology",
            "Sports",
            "Entertainment",
            "Health",
            "Science",
            "World",
            "Education"
        ]

    def classify(
        self,
        text: str
    ):

        if not text:
            return {
                "topic": "Unknown",
                "confidence": 0.0
            }

        # Long articles don't help zero-shot much
        text = " ".join(text.split()[:450])

        result = self.client.inference(
            self.model,
            {
                "inputs": text,
                "parameters": {
                    "candidate_labels": self.labels
                }
            }
        )

        if isinstance(result, list) and len(result) > 0:
            best = result[0]

            return {
                "topic": best["label"],
                "confidence": round(best["score"], 4)
            }

        return {
            "topic": "Unknown",
            "confidence": 0
        }
