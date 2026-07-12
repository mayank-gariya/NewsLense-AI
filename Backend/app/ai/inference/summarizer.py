from app.clients.huggingface_client import HuggingFaceClient


class Summarizer:

    def __init__(self):
        self.client = HuggingFaceClient()
        self.model = "facebook/bart-large-cnn"

    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 800
    ):
        words = text.split()

        chunks = []

        for i in range(0, len(words), chunk_size):
            chunks.append(" ".join(words[i:i + chunk_size]))

        return chunks

    def _summarize_chunk(
        self,
        text: str,
        max_len: int,
        min_len: int
    ):

        result = self.client.inference(
            self.model,
            {
                "inputs": text,
                "parameters": {
                    "max_new_tokens": max_len,
                    "min_length": min_len,
                    "do_sample": False
                }
            }
        )

        if isinstance(result, list):
            return result[0]["summary_text"]

        return result["summary_text"]

    def summarize(
        self,
        text: str,
        max_len: int = 120,
        min_len: int = 40
    ):

        if not text:
            return ""

        text = text.strip()

        # Small article
        if len(text.split()) <= 800:
            return self._summarize_chunk(
                text,
                max_len,
                min_len
            )

        # Long article

        chunks = self._chunk_text(text)

        partial_summaries = []

        for chunk in chunks:

            try:
                partial_summaries.append(
                    self._summarize_chunk(
                        chunk,
                        max_len,
                        min_len
                    )
                )

            except Exception:
                continue

        if not partial_summaries:
            return text[:500]

        combined_summary = " ".join(partial_summaries)

        if len(combined_summary.split()) > 800:

            return self._summarize_chunk(
                combined_summary,
                max_len,
                min_len
            )

        return combined_summary