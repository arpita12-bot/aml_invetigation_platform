"""
==========================================================
AML Investigation Platform

Embedding Repository

Responsibilities
----------------
✓ Load trained embedding models
✓ Load latest model
✓ Load best model
✓ Cache loaded models
✓ Hide filesystem details

==========================================================
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from pykeen.pipeline import PipelineResult

from app.services.knowledge_graph.training.model_registry import (
    ModelRegistryService,
)

logger = logging.getLogger(__name__)


class EmbeddingRepository:
    """
    Repository for loading trained PyKEEN models.
    """

    def __init__(
        self,
        registry: ModelRegistryService,
    ) -> None:

        self._registry = registry

        self._cache: dict[str, PipelineResult] = {}

    def load_best(self) -> PipelineResult:

        registry = self._registry.load()

        if registry.best is None:

            raise RuntimeError(
                "No trained model found."
            )

        return self.load(
            Path(registry.best.model_directory)
        )

    def load_latest(self) -> PipelineResult:

        registry = self._registry.load()

        if registry.latest is None:

            raise RuntimeError(
                "No trained model found."
            )

        return self.load(
            Path(registry.latest.model_directory)
        )

    def load(
        self,
        model_directory: Path,
    ) -> PipelineResult:

        key = str(model_directory)

        if key in self._cache:

            logger.info(
                "Returning cached model %s",
                key,
            )

            return self._cache[key]

        logger.info(
            "Loading PyKEEN model from %s",
            model_directory,
        )

        model = PipelineResult.from_directory(
            model_directory
        )

        self._cache[key] = model

        return model

    def clear_cache(self) -> None:

        self._cache.clear()

    def cached_models(self) -> list[str]:

        return list(self._cache.keys())