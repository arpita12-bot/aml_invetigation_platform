"""
==========================================================
AML Investigation Platform

Schema Inference Service

Responsibilities
----------------
✓ Infer dataset schema
✓ Detect column metadata
✓ Detect semantic metadata
✓ Detect keys
✓ Generate table metadata
✓ Return SchemaInferenceResult

==========================================================
"""

from __future__ import annotations

import time

import pandas as pd

from app.models.schema.graph_metadata import GraphMetadata
from app.models.schema.relationship_metadata import RelationshipMetadata
from app.models.schema.schema_inference_result import (
    SchemaInferenceResult,
)

from app.services.schema.key_detector import KeyDetector
from app.services.schema.schema_generator import SchemaGenerator
from app.services.schema.semantic_detector import SemanticDetector
from app.services.schema.type_inference import TypeInferenceService
from app.models.schema.dataset_metadata import DatasetMetadata

class SchemaInferenceService:
    """
    Orchestrates schema inference.

    This class coordinates all schema inference
    services but does not contain inference logic.
    """

    @classmethod
    def infer(
        cls,
        *,
        dataframe: pd.DataFrame,
        dataset_name: str,
        original_filename: str,
        table_name: str,
        dataset_type: str,
        file_size_mb: float,
        description: str = "",
        source: str = "",
    ) -> SchemaInferenceResult:

        start = time.perf_counter()

        # ------------------------------------------
        # Type Inference
        # ------------------------------------------

        columns = TypeInferenceService.infer(
            dataframe
        )

        # ------------------------------------------
        # Semantic Detection
        # ------------------------------------------

        columns = SemanticDetector.detect(
            columns
        )

        # ------------------------------------------
        # Key Detection
        # ------------------------------------------

        keys = KeyDetector.detect(
            dataframe=dataframe,
            columns=columns,
        )

        # ------------------------------------------
        # Relationship Detection
        # (Implemented later)
        # ------------------------------------------

        relationships: list[
            RelationshipMetadata
        ] = []

        # ------------------------------------------
        # Build Table Metadata
        # ------------------------------------------

        table = SchemaGenerator.generate(

            dataset_name=dataset_name,

            original_filename=original_filename,

            table_name=table_name,

            dataset_type=dataset_type,

            row_count=len(dataframe),

            file_size_mb=file_size_mb,

            columns=columns,

            keys=keys,

            relationships=relationships,

            description=description,

            source=source,

        )

        # ------------------------------------------
        # Graph Metadata
        # ------------------------------------------

        graph = GraphMetadata(

            graph_name=table_name,

            node_labels=[],

            relationship_labels=[],

            relationships=relationships,

        )

        # ------------------------------------------
        # Dataset Metadata
        # ------------------------------------------

        metadata = DatasetMetadata(

            table=table,

            graph=graph,

            profile=None,

            validation=None,

        )

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        return SchemaInferenceResult(

            metadata=metadata,

            inference_time_ms=round(
                elapsed,
                2,
            ),

            successful=True,

            message="Schema inference completed successfully.",

        )