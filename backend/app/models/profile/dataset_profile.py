"""
==========================================================
AML Investigation Platform

Dataset Profile Model

Responsibilities
----------------
✓ Store dataset profiling information
✓ Maintain data quality metrics
✓ Identify entity candidates
✓ Detect primary & foreign key candidates
✓ Support Knowledge Graph generation
✓ Support ML feature engineering

==========================================================
"""

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)

from app.database.base import Base
from sqlalchemy.orm import relationship

class DatasetProfile(Base):
    """
    Stores profiling information for uploaded datasets.
    """

    __tablename__ = "dataset_profile"

    # ======================================================
    # Primary Key
    # ======================================================

    profile_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    # ======================================================
    # Dataset Reference
    # ======================================================

    dataset_id = Column(
        Integer,
        ForeignKey("dataset_registry.dataset_id"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ======================================================
    # Dataset Summary
    # ======================================================

    total_rows = Column(
        Integer,
        nullable=False,
        default=0,
    )

    total_columns = Column(
        Integer,
        nullable=False,
        default=0,
    )

    total_missing_values = Column(
        Integer,
        default=0,
    )

    duplicate_rows = Column(
        Integer,
        default=0,
    )

    duplicate_percentage = Column(
        Float,
        default=0.0,
    )

    quality_score = Column(
        Float,
        default=0.0,
    )

    completeness_score = Column(
        Float,
        default=0.0,
    )

    consistency_score = Column(
        Float,
        default=0.0,
    )

    uniqueness_score = Column(
        Float,
        default=0.0,
    )

    validity_score = Column(
        Float,
        default=0.0,
    )

    # ======================================================
    # Column-Level Profiling
    # ======================================================

    column_profiles = Column(
        JSON,
        nullable=True,
    )

    data_types = Column(
        JSON,
        nullable=True,
    )

    null_percentages = Column(
        JSON,
        nullable=True,
    )

    unique_value_counts = Column(
        JSON,
        nullable=True,
    )

    value_distributions = Column(
        JSON,
        nullable=True,
    )

    # ======================================================
    # Entity Discovery
    # ======================================================

    detected_entities = Column(
        JSON,
        nullable=True,
    )

    entity_columns = Column(
        JSON,
        nullable=True,
    )

    entity_relationship_candidates = Column(
        JSON,
        nullable=True,
    )

    # ======================================================
    # Key Detection
    # ======================================================

    primary_key_candidates = Column(
        JSON,
        nullable=True,
    )

    foreign_key_candidates = Column(
        JSON,
        nullable=True,
    )

    composite_key_candidates = Column(
        JSON,
        nullable=True,
    )

    # ======================================================
    # AML Intelligence
    # ======================================================

    customer_columns = Column(
        JSON,
        nullable=True,
    )

    account_columns = Column(
        JSON,
        nullable=True,
    )

    transaction_columns = Column(
        JSON,
        nullable=True,
    )

    company_columns = Column(
        JSON,
        nullable=True,
    )

    risk_columns = Column(
        JSON,
        nullable=True,
    )

    # ======================================================
    # Graph Readiness
    # ======================================================

    graph_ready = Column(
        Boolean,
        default=False,
    )

    graph_readiness_score = Column(
        Float,
        default=0.0,
    )

    estimated_nodes = Column(
        Integer,
        default=0,
    )

    estimated_relationships = Column(
        Integer,
        default=0,
    )

    # ======================================================
    # Embedding Readiness
    # ======================================================

    embedding_ready = Column(
        Boolean,
        default=False,
    )

    ml_ready = Column(
        Boolean,
        default=False,
    )

    # ======================================================
    # Profiling Report
    # ======================================================

    profile_summary = Column(
        Text,
        nullable=True,
    )

    profiling_report = Column(
        JSON,
        nullable=True,
    )

    recommendations = Column(
        JSON,
        nullable=True,
    )
    
    # ======================================================
    # Relationship
    # ======================================================

    dataset = relationship(
        "DatasetRegistry",
        back_populates="dataset_profile",
        lazy="selectin",
    )