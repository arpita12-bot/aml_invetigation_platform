"""
==========================================================
AML Investigation Platform

Knowledge Graph Training Result

Represents one completed embedding training run.

Shared Across

✓ PyKEEN Trainer
✓ Model Registry
✓ Evaluator
✓ Dashboard
✓ Experiment Tracking

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.models.knowledge_graph.model_type import (
    ModelType,
)

from app.models.knowledge_graph.model_artifact import (
    ModelArtifact,
)

from app.models.knowledge_graph.training_status import (
    TrainingStatus,
)


@dataclass(slots=True)
class TrainingResult:
    """
    Represents one embedding model training result.
    """

    # =====================================================
    # Experiment
    # =====================================================

    experiment_name: str

    model: ModelType

    # =====================================================
    # Dataset
    # =====================================================

    dataset_name: str

    training_triples: int

    validation_triples: int

    testing_triples: int

    # =====================================================
    # Configuration
    # =====================================================

    embedding_dimension: int

    epochs: int

    batch_size: int

    learning_rate: float

    random_seed: int

    # =====================================================
    # Evaluation Metrics
    # =====================================================

    mean_rank: float | None = None

    mean_reciprocal_rank: float | None = None

    hits_at_1: float | None = None

    hits_at_3: float | None = None

    hits_at_10: float | None = None

    training_loss: float | None = None

    # =====================================================
    # Model
    # =====================================================

    artifact: ModelArtifact | None = None

    # =====================================================
    # Execution
    # =====================================================

    started_at: datetime | None = None

    finished_at: datetime | None = None

    execution_time_seconds: float = 0.0

    # =====================================================
    # Status
    # =====================================================

    status: TrainingStatus = (
    TrainingStatus.PENDING
    )

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Helper Properties
    # =====================================================

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    @property
    def is_successful(self) -> bool:
        return (
            self.status
            == TrainingStatus.COMPLETED
            and not self.has_errors
        )

    @property
    def total_triples(self) -> int:
        return (
            self.training_triples
            + self.validation_triples
            + self.testing_triples
        )

    def to_dict(self) -> dict:
        return {

            "experiment_name": self.experiment_name,

            "model": self.model.value,

            "dataset_name": self.dataset_name,

            "training_triples":
                self.training_triples,

            "validation_triples":
                self.validation_triples,

            "testing_triples":
                self.testing_triples,

            "embedding_dimension":
                self.embedding_dimension,

            "epochs":
                self.epochs,

            "batch_size":
                self.batch_size,

            "learning_rate":
                self.learning_rate,

            "random_seed":
                self.random_seed,

            "mean_rank":
                self.mean_rank,

            "mean_reciprocal_rank":
                self.mean_reciprocal_rank,

            "hits_at_1":
                self.hits_at_1,

            "hits_at_3":
                self.hits_at_3,

            "hits_at_10":
                self.hits_at_10,

            "training_loss":
                self.training_loss,

            "execution_time_seconds":
                self.execution_time_seconds,

            "errors":
                self.errors,

            "warnings":
                self.warnings,
                
            "artifact":
                self.artifact.to_dict()
                if self.artifact
                else None,

            "status":
                self.status.value
        }