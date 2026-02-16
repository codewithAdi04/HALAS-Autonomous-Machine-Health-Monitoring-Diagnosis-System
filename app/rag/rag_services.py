from typing import Optional
from app.core.logger import logger


class RAGService:
    """
    Lightweight RAG service (Research-grade stub)

    Purpose:
    - Inject domain knowledge during diagnosis
    - Modular design (can be upgraded to Chroma / FAISS / LangChain)
    """

    def __init__(self):
        # Static knowledge base (health monitoring demo)
        self.knowledge_base = {
            "temperature": "Normal operating temperature should remain below 90°C.",
            "overheat": "Overheating can damage hardware and cause system failure.",
            "error": "System errors may indicate hardware or software faults.",
            "critical": "Critical conditions require immediate attention."
        }

        logger.info("[RAG] RAGService initialized")

    def get_context(self, query: str) -> Optional[str]:
        """
        Retrieve relevant context for a given query.
        """

        query_lower = query.lower()

        for keyword, info in self.knowledge_base.items():
            if keyword in query_lower:
                logger.info(f"[RAG] Context matched for keyword: {keyword}")
                return info

        logger.info("[RAG] No context found")
        return None