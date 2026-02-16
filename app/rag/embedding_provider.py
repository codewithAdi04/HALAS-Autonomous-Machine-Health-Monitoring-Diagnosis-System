from sentence_transformers import SentenceTransformer
from app.rag.config import RAGConfig


class EmbeddingProvider:
    """
    Abstract embedding provider.
    Easily replaceable with OpenAI/Azure later.
    """

    def __init__(self):
        self.model = SentenceTransformer(RAGConfig.EMBEDDING_MODEL)

    def embed(self, texts: list):
        return self.model.encode(texts).tolist()