"""
==========================================================
AML Investigation Platform

Database Base Configuration

Responsibilities
----------------
✓ SQLAlchemy Declarative Base
✓ Common Audit Columns
✓ Automatic Table Naming
✓ Utility Methods

Author : Arpita Kundu
==========================================================
"""

from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy import Column
from sqlalchemy import DateTime


class Base(DeclarativeBase):
    """
    Base class inherited by every ORM model.
    """

    @declared_attr.directive
    def __tablename__(cls):
        """
        Automatically generate table name.

        Example

        DatasetRegistry

        ↓

        dataset_registry
        """

        name = cls.__name__

        table = ""

        for index, char in enumerate(name):

            if char.isupper() and index != 0:
                table += "_"

            table += char.lower()

        return table

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def as_dict(self):
        """
        Convert ORM object to dictionary.
        """

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self):
        values = []

        for column in self.__table__.columns:
            values.append(
                f"{column.name}={getattr(self,column.name)}"
            )

        return (
            f"{self.__class__.__name__}"
            f"({', '.join(values)})"
        )