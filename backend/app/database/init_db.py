"""
==========================================================
AML Investigation Platform

Database Initialization
==========================================================
"""

from app.database.base import Base
from app.database.session import engine

# Register all models
import app.models


def create_tables():
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)