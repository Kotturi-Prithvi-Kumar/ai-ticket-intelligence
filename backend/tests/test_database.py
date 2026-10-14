
from sqlalchemy import text

from app.core.database import get_db


def test_database_session():
    """Verify a database session can execute SQL."""
    session_generator = get_db()

    try:
        session = next(session_generator)
        result = session.execute(text("SELECT 1")).scalar_one()

        assert result == 1
    finally:
        session_generator.close()
