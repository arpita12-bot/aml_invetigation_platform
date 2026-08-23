from __future__ import annotations

import pandas as pd
from sqlalchemy.orm import Session

from app.models.database.database_execution_result import (
    DatabaseExecutionResult,
)
from app.models.schema.dataset_metadata import DatasetMetadata

from app.services.database.postgres_builder import (
    PostgresBuilder,
)
from app.services.database.bulk_loader import (
    BulkLoader,
)
from app.services.graph.graph_generation_service import (
    GraphGenerationService,
)

from app.services.graph.graph_registry_service import GraphRegistryService
from sqlalchemy import text

class DatasetIngestionService:

    @classmethod
    def ingest(
        cls,
        *,
        session: Session,
        dataframe: pd.DataFrame,
        metadata: DatasetMetadata,
        generate_graph: bool = True,
    ) -> DatabaseExecutionResult:

        ddl_result = PostgresBuilder.build(
            session=session,
            metadata=metadata,
        )

        if not ddl_result.successful:
            return ddl_result
        

        # --------------------------------------------------
        # Check if dataset already contains data
        # --------------------------------------------------

        existing_count = session.execute(
            text(
                f"""
                SELECT COUNT(*)
                FROM {metadata.table.table_name}
                """
            )
        ).scalar()

        if existing_count and existing_count > 0:

            result = DatabaseExecutionResult()

            result.successful = False

            result.errors.append(
                f"Dataset '{metadata.table.dataset_name}' has already been uploaded. "
                f"The table '{metadata.table.table_name}' already contains "
                f"{existing_count} records."
            )

            return result

        
        load_result = BulkLoader.load(
            session=session,
            dataframe=dataframe,
            table_name=metadata.table.table_name,
        )

        if not load_result.successful:
            return load_result
        
        primary_keys = metadata.table.primary_keys

        identifier = (
            primary_keys[0].column_name
            if primary_keys
            else dataframe.columns[0]
        )

        display_column = None

        candidate_columns = [
            "name",
            "full_name",
            "company_name",
            "account_number",
        ]

        for column in candidate_columns:

            if column in dataframe.columns:

                display_column = column

                break

        GraphRegistryService(session).register_table(
            table_name=metadata.table.table_name,
            node_label=metadata.table.table_name.title(),
            identifier_column=identifier,
            display_column=display_column,
            entity_type=metadata.table.dataset_name,
        )

        if generate_graph:

            primary_keys = metadata.table.primary_keys

            identifier = (
                primary_keys[0].column_name
                if primary_keys
                else None
            )

            GraphGenerationService(session).generate(
                graph_name="AML_GRAPH",
                dataset_name=metadata.table.dataset_name,
            )

        return load_result