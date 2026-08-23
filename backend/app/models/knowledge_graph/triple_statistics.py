"""
==========================================================
AML Investigation Platform

Triple Statistics

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TripleStatistics:

    total_entities: int = 0

    total_relations: int = 0

    total_triples: int = 0

    unique_heads: int = 0

    unique_tails: int = 0

    relation_frequency: dict[str, int] = field(
        default_factory=dict
    )

    entity_frequency: dict[str, int] = field(
        default_factory=dict
    )