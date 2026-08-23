"""
==========================================================
AML Investigation Platform

Training Configuration

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.knowledge_graph.model_type import (
    ModelType,
)
from pathlib import Path


@dataclass(slots=True)
class TrainingConfig:
    """
    Configuration for PyKEEN training.
    """

    # --------------------------------------------------
    # Model
    # --------------------------------------------------

    model: ModelType = ModelType.TRANSE

    # --------------------------------------------------
    # Embeddings
    # --------------------------------------------------

    embedding_dimension: int = 200

    # --------------------------------------------------
    # Optimizer
    # --------------------------------------------------

    learning_rate: float = 0.001

    batch_size: int = 1024

    num_epochs: int = 100

    # --------------------------------------------------
    # Reproducibility
    # --------------------------------------------------

    random_seed: int = 42

    # --------------------------------------------------
    # Device
    # --------------------------------------------------

    use_gpu: bool = True

    # --------------------------------------------------
    # Output
    # --------------------------------------------------

    save_directory: str = "models"

    experiment_name: str = "default"

    root_output_directory: Path = Path("models")
    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    @property
    def device(self) -> str:

        return "cuda" if self.use_gpu else "cpu"