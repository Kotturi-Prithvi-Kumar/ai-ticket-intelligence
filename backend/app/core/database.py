
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings

settings = get_settings()

engine = (
    create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=0,
    )
    if settings.database_url
    else None
)

SessionLocal = (
    sessionmaker(bind=engine, autoflush=False)
    if engine is not None
    else None
)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session and close it after use."""
    if SessionLocal is None:
        raise RuntimeError("Database is not configured")

    with SessionLocal() as session:
        yield session