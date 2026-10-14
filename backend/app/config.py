
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Resolve the project root independently of the terminal directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load local environment variables without overriding existing values.
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = "AI ticket intelligence API"
    app_version: str = "0.1.0"
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = ""


def get_settings() -> Settings:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    database = os.getenv("POSTGRES_DB")
    port = os.getenv("POSTGRES_PORT", "5433")

    database_url = ""

    if all([user, password, database]):
        from sqlalchemy.engine import URL

        database_url = URL.create(
            drivername="postgresql+psycopg",
            username=user,
            password=password,
            host="127.0.0.1",
            port=int(port),
            database=database,
        ).render_as_string(hide_password=False)

    return Settings(
        environment=os.getenv("APP_ENV", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        database_url=database_url,
    )
