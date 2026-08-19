import os
import yaml
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, config_path: str = None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(base_dir, "config", "config.yml")

        with open(config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

    @property
    def app_name(self) -> str:
        return self._config["app"]["name"]

    @property
    def app_version(self) -> str:
        return self._config["app"]["version"]

    @property
    def model_provider(self) -> str:
        return self._config["models"]["provider"]

    @property
    def model_name(self) -> str:
        return self._config["models"]["model_name"]

    @property
    def some_secret_key(self) -> str:
        
        return os.getenv("MY_API_KEY", "")

settings = Config()