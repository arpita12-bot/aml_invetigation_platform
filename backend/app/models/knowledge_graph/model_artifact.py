"""
==========================================================
AML Investigation Platform

Model Artifact

Represents all artifacts generated after
training a Knowledge Graph Embedding model.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True)
class ModelArtifact:
    """
    Stores all files produced by a training run.
    """

    # -----------------------------------------------------
    # Model
    # -----------------------------------------------------

    model_directory: Path

    model_file: Path

    # -----------------------------------------------------
    # Embeddings
    # -----------------------------------------------------

    entity_embeddings: Path | None = None

    relation_embeddings: Path | None = None

    # -----------------------------------------------------
    # Metadata
    # -----------------------------------------------------

    config_file: Path | None = None

    metrics_file: Path | None = None

    training_log: Path | None = None

    # -----------------------------------------------------
    # Helper
    # -----------------------------------------------------

    def to_dict(self) -> dict:

        return {
            "model_directory": str(self.model_directory),
            "model_file": str(self.model_file),
            "entity_embeddings": (
                str(self.entity_embeddings)
                if self.entity_embeddings
                else None
            ),
            "relation_embeddings": (
                str(self.relation_embeddings)
                if self.relation_embeddings
                else None
            ),
            "config_file": (
                str(self.config_file)
                if self.config_file
                else None
            ),
            "metrics_file": (
                str(self.metrics_file)
                if self.metrics_file
                else None
            ),
            "training_log": (
                str(self.training_log)
                if self.training_log
                else None
            ),
        }