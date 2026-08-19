from functools import lru_cache
from src.config.config_parser import settings
from src.logging.logger import logger

class DummyModel:
    """موديل وهمي عشان نوضح إن الـ instantiation بيحصل مرة واحدة بس."""
    def __init__(self, name: str):
        self.name = name

    def predict(self, text: str) -> str:
        return f"[{self.name}] echo: {text}"

class ModelFactory:
    """
    Factory + Singleton (@lru_cache) عشان نضمن إن الموديل
    مش بيتحمّل من تاني مع كل request.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def get_model():
        logger.info(f"Initializing model (Provider: {settings.model_provider}, Name: {settings.model_name})...")
        return DummyModel(settings.model_name)