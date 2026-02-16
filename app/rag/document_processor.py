from app.rag.config import RAGConfig


class DocumentProcessor:
    """
    Handles text chunking for RAG ingestion.
    """

    def chunk_text(self, text: str):

        chunk_size = RAGConfig.CHUNK_SIZE
        overlap = RAGConfig.CHUNK_OVERLAP

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap

        return chunks