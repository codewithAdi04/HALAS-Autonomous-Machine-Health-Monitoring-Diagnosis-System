class RAGConfig:
    COLLECTION_NAME = "halas_knowledge"
    PERSIST_DIRECTORY = "./halas_chroma_db"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50