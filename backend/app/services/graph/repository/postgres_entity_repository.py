"""
==========================================================
AML Investigation Platform

PostgreSQL Entity Repository

Responsibilities
----------------
✓ Read business entities from PostgreSQL
✓ Return dictionaries (not ORM objects)
✓ Keep graph layer database-independent

==========================================================
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session


class PostgresEntityRepository:
    """
    Repository responsible for reading AML business data
    from PostgreSQL.

    Returns plain dictionaries to keep the graph layer
    independent of ORM models.
    """

    def __init__(self, session: Session):
        self._session = session

    # -----------------------------------------------------
    # Generic helper
    # -----------------------------------------------------

    def _fetch_all(self, table_name: str) -> list[dict]:

        result = self._session.execute(
            text(f"SELECT * FROM {table_name}")
        )

        return [
            dict(row._mapping)
            for row in result
        ]

    # -----------------------------------------------------
    # Customers
    # -----------------------------------------------------

    def customers(self) -> list[dict]:
        return self._fetch_all("customers")

    # -----------------------------------------------------
    # Accounts
    # -----------------------------------------------------

    def accounts(self) -> list[dict]:
        return self._fetch_all("accounts")

    # -----------------------------------------------------
    # Transactions
    # -----------------------------------------------------

    def transactions(self) -> list[dict]:
        return self._fetch_all("transactions")

    # -----------------------------------------------------
    # Companies
    # -----------------------------------------------------

    def companies(self) -> list[dict]:
        return self._fetch_all("companies")

    # -----------------------------------------------------
    # Devices
    # -----------------------------------------------------

    def devices(self) -> list[dict]:
        return self._fetch_all("devices")

    # -----------------------------------------------------
    # IP Addresses
    # -----------------------------------------------------

    def ip_addresses(self) -> list[dict]:
        return self._fetch_all("ip_addresses")

    # -----------------------------------------------------
    # PEP
    # -----------------------------------------------------

    def pep(self) -> list[dict]:
        return self._fetch_all("pep")

    # -----------------------------------------------------
    # Sanctions
    # -----------------------------------------------------

    def sanctions(self) -> list[dict]:
        return self._fetch_all("sanctions")

    # -----------------------------------------------------
    # Watchlists
    # -----------------------------------------------------

    def watchlists(self) -> list[dict]:
        return self._fetch_all("watchlists")

    # -----------------------------------------------------
    # Adverse News
    # -----------------------------------------------------

    def adverse_news(self) -> list[dict]:
        return self._fetch_all("adverse_news")