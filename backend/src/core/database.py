"""Database connection and session management.

Per Constitution V: All data MUST be persisted in Neon Serverless PostgreSQL.
Per Constitution V: Database schema MUST be managed via SQLModel ORM.
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

from .config import settings

# Create database engine
# Use connect_args for PostgreSQL connection pooling compatibility
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,  # Verify connections before use
)


def get_session() -> Generator[Session, None, None]:
    """Get a database session.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables() -> None:
    """Create all database tables from SQLModel metadata.

    Called on application startup to ensure schema exists.
    """
    SQLModel.metadata.create_all(engine)
