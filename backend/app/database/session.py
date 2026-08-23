"""
==========================================================
AML Investigation Platform

Database Session

Responsibilities
----------------
✓ Create SQLAlchemy Engine
✓ Create Session Factory
✓ FastAPI Dependency
==========================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.postgres_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    """
    FastAPI database dependency.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()