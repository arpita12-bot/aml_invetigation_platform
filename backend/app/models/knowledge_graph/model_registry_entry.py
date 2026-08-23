"""
==========================================================
AML Investigation Platform

Model Registry Entry

Represents one registered embedding model.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.models.knowledge_graph.model_type import ModelType


@dataclass(slots=True)
class ModelRegistryEntry:

    experiment_name: str

    version: str

    model: ModelType

    dataset_name: str

    model_directory: str

    model_file: str

    mean_reciprocal_rank: float | None = None

    hits_at_10: float | None = None

    created_at: datetime | None = None

    is_best: bool = False

    def to_dict(self) -> dict:

        return {

            "experiment_name":
                self.experiment_name,

            "version":
                self.version,

            "model":
                self.model.value,

            "dataset_name":
                self.dataset_name,

            "model_directory":
                self.model_directory,

            "model_file":
                self.model_file,

            "mean_reciprocal_rank":
                self.mean_reciprocal_rank,

            "hits_at_10":
                self.hits_at_10,

            "created_at":
                self.created_at.isoformat()
                if self.created_at
                else None,

            "is_best":
                self.is_best,
        }