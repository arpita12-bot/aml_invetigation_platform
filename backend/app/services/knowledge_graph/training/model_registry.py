"""
==========================================================
AML Investigation Platform

Model Registry Service

Responsibilities
----------------
✓ Register model
✓ Save registry
✓ Load registry
✓ Return latest model
✓ Return best model

==========================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from app.models.knowledge_graph.model_registry import (
    ModelRegistry,
)
from app.models.knowledge_graph.model_registry_entry import (
    ModelRegistryEntry,
)
from app.models.knowledge_graph.training_result import (
    TrainingResult,
)


class ModelRegistryService:

    REGISTRY_FILE = "registry.json"

    def __init__(self, registry_directory: Path):

        self.registry_directory = registry_directory

        self.registry_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.registry_path = (
            self.registry_directory
            / self.REGISTRY_FILE
        )

    def register(
        self,
        result: TrainingResult,
        version: str,
    ) -> None:

        registry = self.load()

        entry = ModelRegistryEntry(

            experiment_name=result.experiment_name,

            version=version,

            model=result.model,

            dataset_name=result.dataset_name,

            model_directory=str(
                result.artifact.model_directory
            ),

            model_file=str(
                result.artifact.model_file
            ),

            mean_reciprocal_rank=result.mean_reciprocal_rank,

            hits_at_10=result.hits_at_10,

            created_at=datetime.utcnow(),
        )

        registry.models.append(entry)

        best = registry.best

        if best is not None:
            for model in registry.models:
                model.is_best = (
                    model.version == best.version
                )

        self.save(registry)

    def save(
        self,
        registry: ModelRegistry,
    ) -> None:

        with open(
            self.registry_path,
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                registry.to_dict(),
                fp,
                indent=4,
            )

    def load(self) -> ModelRegistry:

        if not self.registry_path.exists():
            return ModelRegistry()

        with open(
            self.registry_path,
            "r",
            encoding="utf-8",
        ) as fp:

            data = json.load(fp)

        registry = ModelRegistry()

        for item in data.get("models", []):

            registry.models.append(

                ModelRegistryEntry(

                    experiment_name=item["experiment_name"],

                    version=item["version"],

                    model=item["model"],

                    dataset_name=item["dataset_name"],

                    model_directory=item["model_directory"],

                    model_file=item["model_file"],

                    mean_reciprocal_rank=item.get(
                        "mean_reciprocal_rank"
                    ),

                    hits_at_10=item.get(
                        "hits_at_10"
                    ),

                    created_at=datetime.fromisoformat(
                        item["created_at"]
                    )
                    if item["created_at"]
                    else None,

                    is_best=item.get(
                        "is_best",
                        False,
                    ),
                )

            )

        return registry