from app.rag.vector_store import VectorStore
from app.rag.document_processor import DocumentProcessor
from app.core.logger import logger


class Retriever:
    """
    Handles knowledge ingestion and retrieval.
    """

    def __init__(self):
        self.vector_store = VectorStore()
        self.processor = DocumentProcessor()

    def ingest_document(self, raw_text: str, source: str = "manual"):

        chunks = self.processor.chunk_text(raw_text)

        metadata = [{"source": source} for _ in chunks]

        self.vector_store.add_documents(chunks, metadata)

        logger.info(f"[RAG] Ingested {len(chunks)} chunks")

    def retrieve(self, query: str, top_k: int = 5):

        try:
            results = self.vector_store.query(query, top_k)
            logger.info(f"[RAG] Retrieved {len(results)} documents")
            return "\n".join(results)
        except Exception as e:
            logger.error(f"[RAG] Retrieval failed: {str(e)}")
            return ""