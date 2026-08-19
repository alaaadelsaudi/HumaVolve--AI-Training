from functools import lru_cache
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.config_parser import settings
from src.logging.logger import logger

class ModelFactory:
    """
    Factory Pattern + Singleton (@lru_cache) لتحميل الموديلات الثقيلة مرة واحدة بس.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def get_embeddings():
        if settings.embedding_provider.lower() == "huggingface":
            logger.info(f"Initializing Embeddings Model ({settings.embedding_model_name})...")
            return HuggingFaceEmbeddings(
                model_name=settings.embedding_model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")

    @staticmethod
    @lru_cache(maxsize=1)
    def get_llm():
        if settings.llm_provider.lower() == "gemini":
            logger.info(f"Initializing LLM ({settings.llm_model_name})...")
            return ChatGoogleGenerativeAI(
                model=settings.llm_model_name,
                temperature=settings.temperature,
                google_api_key=settings.google_api_key
            )
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")