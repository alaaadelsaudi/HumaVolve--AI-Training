import os
from langchain_community.vectorstores import FAISS
from src.core.factories import ModelFactory
from src.config.config_parser import settings
from src.logging.logger import logger

class VectorDatabaseRepository:
    """Repository Layer لإدارة FAISS، مع Singleton caching في الذاكرة."""
    _instance_cache = None

    def __init__(self):
        self.embeddings = ModelFactory.get_embeddings()
        self.index_path = settings.vector_index_path

    def save_index(self, vectorstore: FAISS):
        logger.info(f"Saving FAISS index to '{self.index_path}'...")
        vectorstore.save_local(self.index_path)
        VectorDatabaseRepository._instance_cache = vectorstore

    def load_index(self) -> FAISS:
        if VectorDatabaseRepository._instance_cache is not None:
            logger.info("Using in-memory cached FAISS index.")
            return VectorDatabaseRepository._instance_cache

        if not os.path.exists(self.index_path):
            raise FileNotFoundError(
                f"FAISS index '{self.index_path}' not found! Call /api/v1/ingest first."
            )

        logger.info(f"Loading FAISS index from disk '{self.index_path}'...")
        vectorstore = FAISS.load_local(
            self.index_path, self.embeddings, allow_dangerous_deserialization=True
        )
        VectorDatabaseRepository._instance_cache = vectorstore
        return vectorstore

    def create_from_documents(self, documents: list, batch_size: int = None) -> FAISS:
        batch_size = batch_size or settings.batch_size
        total = len(documents)
        vectorstore = None

        for i in range(0, total, batch_size):
            batch = documents[i:i + batch_size]
            logger.info(f"Embedding batch {i // batch_size + 1} ({len(batch)} chunks)...")
            if vectorstore is None:
                vectorstore = FAISS.from_documents(batch, self.embeddings)
            else:
                vectorstore.add_documents(batch)

        self.save_index(vectorstore)
        return vectorstore