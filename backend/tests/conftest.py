
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.database import get_db
from app.main import app


TEST_DATABASE_NAME = "ticket_intelligence_test"


@pytest.fixture
def db_session():
    """Provide an isolated PostgreSQL transaction for each test."""
    settings = get_settings()

    if not settings.database_url:
        raise RuntimeError("Database URL is not configured")

    database_url = make_url(settings.database_url).set(
        database=TEST_DATABASE_NAME
    )

    if database_url.database != TEST_DATABASE_NAME:
        raise RuntimeError("Refusing to use a non-test database")

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
    )

    try:
        with engine.connect() as connection:
            transaction = connection.begin()

            # Confirm the actual connected database.
            actual_database = connection.execute(
                text("SELECT current_database()")
            ).scalar_one()

            if actual_database != TEST_DATABASE_NAME:
                raise RuntimeError(
                    "Connected to an unexpected database"
                )


            session = Session(
                bind=connection,
                join_transaction_mode="create_savepoint",
            )

            try:
                yield session
            finally:
                session.close()
                transaction.rollback()
    finally:
        engine.dispose()


@pytest.fixture
def client(db_session):
    """Create a test client using the isolated database session."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
