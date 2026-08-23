"""
==========================================================
AML Investigation Platform

Knowledge Graph Triple

Represents one (Head, Relation, Tail) triple
used by PyKEEN and Knowledge Graph Embeddings.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Triple:
    """
    Represents one knowledge graph triple.

    Example
    -------
    Customer001
        OWNS
    Account1001
    """

    # -----------------------------------------------------
    # Triple
    # -----------------------------------------------------

    head: str

    relation: str

    tail: str

    # -----------------------------------------------------
    # Metadata
    # -----------------------------------------------------

    confidence: float = 1.0

    source_table: str = ""

    target_table: str = ""

    inferred: bool = False

    properties: dict = field(
        default_factory=dict
    )

    # -----------------------------------------------------
    # Helper
    # -----------------------------------------------------

    def as_tuple(self) -> tuple[str, str, str]:

        return (
            self.head,
            self.relation,
            self.tail,
        )

    def to_dict(self) -> dict:

        return {

            "head": self.head,

            "relation": self.relation,

            "tail": self.tail,

            "confidence": self.confidence,

            "source_table": self.source_table,

            "target_table": self.target_table,

            "inferred": self.inferred,

            "properties": self.properties,

        }