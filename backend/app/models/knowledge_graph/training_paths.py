"""
==========================================================
AML Investigation Platform

Training Paths

Centralizes all filesystem locations used by the
Knowledge Graph training pipeline.

Responsibilities
----------------
✓ Model storage
✓ Experiment folders
✓ Metrics
✓ Logs
✓ Configuration
✓ Embeddings

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class TrainingPaths:
    """
    Filesystem layout for one experiment.
    """

    root_directory: Path

    experiment_name: str

    @property
    def experiment_directory(self) -> Path:
        return self.root_directory / self.experiment_name

    @property
    def model_directory(self) -> Path:
        return self.experiment_directory / "model"

    @property
    def embedding_directory(self) -> Path:
        return self.experiment_directory / "embeddings"

    @property
    def metrics_directory(self) -> Path:
        return self.experiment_directory / "metrics"

    @property
    def log_directory(self) -> Path:
        return self.experiment_directory / "logs"

    @property
    def config_directory(self) -> Path:
        return self.experiment_directory / "config"

    @property
    def model_file(self) -> Path:
        return self.model_directory / "trained_model.pkl"

    @property
    def entity_embedding_file(self) -> Path:
        return self.embedding_directory / "entity_embeddings.npy"

    @property
    def relation_embedding_file(self) -> Path:
        return self.embedding_directory / "relation_embeddings.npy"

    @property
    def metrics_file(self) -> Path:
        return self.metrics_directory / "metrics.json"

    @property
    def config_file(self) -> Path:
        return self.config_directory / "training_config.json"

    @property
    def log_file(self) -> Path:
        return self.log_directory / "training.log"