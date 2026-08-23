"""
==========================================================
AML Investigation Platform

User ORM Model
==========================================================
"""

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class User(Base):

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    username = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    email = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    hashed_password = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        String(50),
        nullable=False,
        default="ANALYST",
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )