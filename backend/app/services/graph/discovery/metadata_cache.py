"""
==========================================================
AML Investigation Platform

Metadata Cache

Responsibilities
----------------
✓ Load metadata once
✓ Cache Graph Registry
✓ Cache Dataset Registry
✓ Cache PK/FK metadata
✓ Provide fast metadata lookups

==========================================================
"""

from __future__ import annotations

import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.graph_registry import GraphRegistry
from app.repositories.dataset_registry_repository import (
    DatasetRegistryRepository,
)

logger = logging.getLogger(__name__)


class MetadataCache:
    """
    Central metadata cache used by graph discovery.

    This class performs all required metadata queries once,
    then exposes fast dictionary lookups to discovery
    providers.
    """

    def __init__(self, db: Session):

        self.db = db

        self.dataset_repository = DatasetRegistryRepository(db)

        self.loaded = False

        # -----------------------------
        # Registry caches
        # -----------------------------

        self.datasets = {}

        self.graph_registry = {}

        # -----------------------------
        # Database metadata
        # -----------------------------

        self.primary_keys = {}

        self.foreign_keys = {}

    # =====================================================
    # Public
    # =====================================================

    def load(self) -> None:

        if self.loaded:
            return

        self._load_dataset_registry()

        self._load_graph_registry()

        self._load_database_metadata()

        self.loaded = True

        logger.info(
            "Metadata cache loaded successfully."
        )

    # =====================================================
    # Dataset Registry
    # =====================================================

    def _load_dataset_registry(self):

        datasets = (
            self.dataset_repository
            .list_active_datasets()
        )

        self.datasets = {

            dataset.table_name: dataset

            for dataset in datasets

        }

    # =====================================================
    # Graph Registry
    # =====================================================

    def _load_graph_registry(self):

        rows = (

            self.db.query(GraphRegistry)

            .filter(
                GraphRegistry.is_active.is_(True)
            )

            .filter(
                GraphRegistry.include_in_graph.is_(True)
            )

            .all()

        )

        self.graph_registry = {

            row.table_name: row

            for row in rows

        }

    # =====================================================
    # PostgreSQL Metadata
    # =====================================================

    def _load_database_metadata(self):

        self._load_primary_keys()

        self._load_foreign_keys()

    # -----------------------------------------------------

    def _load_primary_keys(self):

        sql = text(
            """
            SELECT

                tc.table_name,

                kcu.column_name

            FROM information_schema.table_constraints tc

            JOIN information_schema.key_column_usage kcu

                 ON tc.constraint_name = kcu.constraint_name

            WHERE tc.constraint_type='PRIMARY KEY';
            """
        )

        rows = self.db.execute(sql)

        for table_name, column_name in rows:

            self.primary_keys.setdefault(
                table_name,
                []
            ).append(column_name)

    # -----------------------------------------------------

    def _load_foreign_keys(self):

        sql = text(
            """
            SELECT

                tc.table_name,

                kcu.column_name,

                ccu.table_name,

                ccu.column_name

            FROM information_schema.table_constraints tc

            JOIN information_schema.key_column_usage kcu

                 ON tc.constraint_name = kcu.constraint_name

            JOIN information_schema.constraint_column_usage ccu

                 ON ccu.constraint_name = tc.constraint_name

            WHERE tc.constraint_type='FOREIGN KEY';
            """
        )

        rows = self.db.execute(sql)

        for row in rows:

            self.foreign_keys.setdefault(
                row[0],
                []
            ).append(

                {

                    "source_column": row[1],

                    "target_table": row[2],

                    "target_column": row[3],

                }

            )

    # =====================================================
    # Lookup Helpers
    # =====================================================

    def dataset(self, table_name):

        return self.datasets.get(table_name)

    # -----------------------------------------------------

    def graph(self, table_name):

        return self.graph_registry.get(table_name)

    # -----------------------------------------------------

    def pk(self, table_name):

        return self.primary_keys.get(table_name, [])

    # -----------------------------------------------------

    def fk(self, table_name):

        return self.foreign_keys.get(table_name, [])