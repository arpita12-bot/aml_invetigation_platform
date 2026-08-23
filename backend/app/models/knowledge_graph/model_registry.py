"""
==========================================================
AML Investigation Platform

Model Registry

Stores all registered models.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.knowledge_graph.model_registry_entry import (
    ModelRegistryEntry,
)


@dataclass(slots=True)
class ModelRegistry:

    models: list[ModelRegistryEntry] = field(
        default_factory=list
    )

    @property
    def latest(self) -> ModelRegistryEntry | None:

        if not self.models:
            return None

        return self.models[-1]

    @property
    def best(self) -> ModelRegistryEntry | None:

        candidates = [
            m
            for m in self.models
            if m.mean_reciprocal_rank is not None
        ]

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda x: x.mean_reciprocal_rank,
        )

    def to_dict(self) -> dict:

        return {

            "models":
                [
                    m.to_dict()
                    for m in self.models
                ]
        }