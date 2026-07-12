from app.clients.huggingface_client import HuggingFaceClient


class QuestionAnswering:

    def __init__(self):
        self.client = HuggingFaceClient()
        self.model = "deepset/roberta-base-squad2"

    def _chunk_context(
        self,
        context: str,
        chunk_size: int = 450
    ):
        """
        Split long articles into chunks.
        QA models cannot handle very long contexts.
        """
        words = context.split()

        chunks = []

        for i in range(0, len(words), chunk_size):
            chunks.append(
                " ".join(words[i:i + chunk_size])
            )

        return chunks

    def answer(
        self,
        question: str,
        context: str
    ):

        if not question or not context:
            return {
                "answer": "",
                "confidence": 0.0
            }

        chunks = self._chunk_context(context)

        best_answer = ""
        best_score = 0

        for chunk in chunks:

            try:

                result = self.client.inference(
                    self.model,
                    {
                        "inputs": {
                            "question": question,
                            "context": chunk
                        }
                    }
                )

                if result["score"] > best_score:
                    best_score = result["score"]
                    best_answer = result["answer"]

            except Exception:
                continue

        return {
            "answer": best_answer,
            "confidence": round(best_score, 4)
        }