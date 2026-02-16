import chromadb
from chromadb.config import Settings
import uuid

from app.rag.config import RAGConfig
from app.rag.embedding_provider import EmbeddingProvider


class VectorStore:
    """
    Production-ready persistent vector store.
    """

    def __init__(self):

        self.embedding_provider = EmbeddingProvider()

        self.client = chromadb.Client(
            Settings(
                persist_directory=RAGConfig.PERSIST_DIRECTORY,
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=RAGConfig.COLLECTION_NAME
        )

    def add_documents(self, texts: list, metadata: list = None):

        embeddings = self.embedding_provider.embed(texts)

        ids = [str(uuid.uuid4()) for _ in texts]

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadata
        )

        self.client.persist()

    def query(self, query_text: str, top_k: int = 5):

        query_embedding = self.embedding_provider.embed([query_text])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results.get("documents", [[]])[0]