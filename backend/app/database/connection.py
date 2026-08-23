"""
==========================================================
AML Investigation Platform

Database Connection Management

Responsibilities
----------------
✓ Create SQLAlchemy Engine
✓ Configure Connection Pool
✓ Create Session Factory
✓ FastAPI Database Dependency
✓ Database Initialization
✓ Database Health Check

==========================================================
"""

from typing import Generator
# Import all ORM models so SQLAlchemy registers them
from app.models import *
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.database.base import Base


# ==========================================================
# SQLAlchemy Engine
# ==========================================================

engine = create_engine(
    settings.postgres_url,
    echo=settings.DEBUG,
    future=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,
)


# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


# ==========================================================
# Database Dependency
# ==========================================================

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency.

    Usage:

    db: Session = Depends(get_db)
    """

    db = SessionLocal()

    try:
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


# ==========================================================
# Database Initialization
# ==========================================================

def init_db() -> None:
    """
    Create all metadata tables.

    NOTE:
    Dynamic uploaded dataset tables will NOT be
    created here. They are created at runtime.
    """

    Base.metadata.create_all(bind=engine)


# ==========================================================
# Database Health Check
# ==========================================================

def check_database_connection() -> bool:
    """
    Verify PostgreSQL connectivity.
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except SQLAlchemyError:
        return False


# ==========================================================
# Utility Function
# ==========================================================

def get_session() -> Session:
    """
    Create a standalone database session.

    Useful for background jobs, scripts,
    and scheduled tasks.
    """

    return SessionLocal()