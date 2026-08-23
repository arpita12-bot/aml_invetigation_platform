"""
==========================================================
AML Investigation Platform

Relationship Metadata

Shared Across

✓ Schema Inference
✓ PostgreSQL
✓ Neo4j
✓ PyKEEN
✓ GNN
✓ Entity Resolution

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RelationshipMetadata:

    # =====================================================
    # Source Schema
    # =====================================================

    source_table: str
    source_column: str
    source_entity: str

    # =====================================================
    # Target Schema
    # =====================================================

    target_table: str
    target_column: str
    target_entity: str

    # =====================================================
    # Relationship
    # =====================================================

    relationship_name: str
    relationship_type: str

    cardinality: str = "MANY_TO_ONE"

    confidence: float = 1.0

    inferred: bool = True

    # =====================================================
    # Neo4j Source Node
    # =====================================================

    source_label: str = ""

    source_identifier: str = ""

    source_identifier_value: str = ""

    # =====================================================
    # Neo4j Target Node
    # =====================================================

    target_label: str = ""

    target_identifier: str = ""

    target_identifier_value: str = ""

    # =====================================================
    # Neo4j Relationship
    # =====================================================

    neo4j_relationship: str = ""

    directed: bool = True

    properties: dict = field(
        default_factory=dict
    )

    # =====================================================
    # Validation
    # =====================================================

    valid: bool = True

    validation_errors: list[str] = field(
        default_factory=list
    )

    validation_warnings: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Helper
    # =====================================================

    def to_dict(self):

        return {

            # Schema

            "source_table": self.source_table,

            "source_column": self.source_column,

            "source_entity": self.source_entity,

            "target_table": self.target_table,

            "target_column": self.target_column,

            "target_entity": self.target_entity,

            # Relationship

            "relationship_name": self.relationship_name,

            "relationship_type": self.relationship_type,

            "cardinality": self.cardinality,

            "confidence": self.confidence,

            "inferred": self.inferred,

            # Neo4j

            "source_label": self.source_label,

            "source_identifier": self.source_identifier,

            "source_identifier_value":
                self.source_identifier_value,

            "target_label": self.target_label,

            "target_identifier":
                self.target_identifier,

            "target_identifier_value":
                self.target_identifier_value,

            "neo4j_relationship":
                self.neo4j_relationship,

            "directed": self.directed,

            "properties": self.properties,

            # Validation

            "valid": self.valid,

            "validation_errors":
                self.validation_errors,

            "validation_warnings":
                self.validation_warnings,

        }