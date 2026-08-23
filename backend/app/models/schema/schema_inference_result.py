"""
==========================================================
AML Investigation Platform

Schema Inference Result

Returned by the Schema Inference Engine.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.schema.dataset_metadata import DatasetMetadata

@dataclass(slots=True)
class SchemaInferenceResult:
    """
    Complete schema inference output.
    """

    metadata: DatasetMetadata

    inference_time_ms: float = 0.0

    successful: bool = True

    message: str = ""