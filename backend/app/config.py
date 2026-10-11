import os 
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_name : str = "AI ticket intelligence API"
    app_version : str = "0.1.0"
    environment : str = "Development"
    log_level : str = "INFO"

def get_settings() -> Settings:
    return Settings(
        environment = os.getenv("APP_ENV", "development"),
        log_level = os.getenv("LOG_LEVEL","INFO").upper(),
    )