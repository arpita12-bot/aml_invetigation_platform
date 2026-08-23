"""
==========================================================
AML Investigation Platform

Dataset Registry Model

Responsibilities
----------------
✓ Register every uploaded dataset
✓ Track upload status
✓ Store file metadata
✓ Track PostgreSQL table mapping
✓ Prevent duplicate uploads
✓ Support incremental loading

==========================================================
"""
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.sql import func
from app.database.base import Base
from sqlalchemy import Enum

from app.core.constants import (
    UploadStatus,
    ValidationStatus,
    ProcessingStatus,
)

class DatasetRegistry(Base):
    """
    Metadata for every uploaded dataset.
    """

    __tablename__ = "dataset_registry"

    # ======================================================
    # Primary Key
    # ======================================================

    dataset_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    # ======================================================
    # File Information
    # ======================================================

    original_filename = Column(
        String(255),
        nullable=False,
    )

    sanitized_filename = Column(
        String(255),
        nullable=False,
    )

    file_extension = Column(
        String(20),
        nullable=False,
    )

    file_size_bytes = Column(
        Integer,
        nullable=False,
    )

    file_hash = Column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
    )

    upload_path = Column(
        String(500),
        nullable=False,
    )

    # ======================================================
    # PostgreSQL Information
    # ======================================================

    table_name = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    schema_name = Column(
        String(100),
        default="public",
        nullable=False,
    )

    # ======================================================
    # Dataset Statistics
    # ======================================================

    total_rows = Column(
        Integer,
        default=0,
        nullable=False,
    )

    total_columns = Column(
        Integer,
        default=0,
        nullable=False,
    )

    inserted_rows = Column(
        Integer,
        default=0,
        nullable=False,
    )

    skipped_rows = Column(
        Integer,
        default=0,
        nullable=False,
    )

    duplicate_rows = Column(
        Integer,
        default=0,
        nullable=False,
    )

    # ======================================================
    # Upload Status
    # ======================================================

    upload_status = Column(
    Enum(UploadStatus, name="upload_status_enum"),
    default=UploadStatus.PENDING,
    nullable=False,
    )
    
    validation_status = Column(
    Enum(ValidationStatus, name="validation_status_enum"),
    default=ValidationStatus.PENDING,
    nullable=False,
    )

    processing_status = Column(
    Enum(ProcessingStatus, name="processing_status_enum"),
    default=ProcessingStatus.PENDING,
    nullable=False,
    )

    # ======================================================
    # Data Quality
    # ======================================================

    quality_score = Column(
        Float,
        default=0.0,
    )

    null_percentage = Column(
        Float,
        default=0.0,
    )

    duplicate_percentage = Column(
        Float,
        default=0.0,
    )

    # ======================================================
    # Schema Information
    # ======================================================

    detected_schema = Column(
        JSON,
        nullable=True,
    )

    detected_primary_keys = Column(
        JSON,
        nullable=True,
    )

    detected_foreign_keys = Column(
        JSON,
        nullable=True,
    )

    detected_entities = Column(
        JSON,
        nullable=True,
    )

    # ======================================================
    # Processing Information
    # ======================================================

    uploaded_by = Column(
        String(100),
        nullable=True,
    )

    processing_time_seconds = Column(
        Float,
        default=0.0,
    )

    last_processed_at = Column(
        DateTime,
        nullable=True,
    )

    # ======================================================
    # Graph Processing
    # ======================================================

    graph_created = Column(
        Boolean,
        default=False,
    )

    graph_nodes = Column(
        Integer,
        default=0,
    )

    graph_edges = Column(
        Integer,
        default=0,
    )

    embeddings_generated = Column(
        Boolean,
        default=False,
    )

    link_prediction_completed = Column(
        Boolean,
        default=False,
    )

    # ======================================================
    # Additional Metadata
    # ======================================================

    tags = Column(
        JSON,
        nullable=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    remarks = Column(
        Text,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    # ======================================================
    # Relationships
    # ======================================================

    upload_audits = relationship(
        "UploadAudit",
        back_populates="dataset",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    dataset_profile = relationship(
        "DatasetProfile",
        back_populates="dataset",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    
    dataset_name = Column(
        String(255),
        nullable=False,
        index=True,
    )
    
    mime_type = Column(
        String(100),
        nullable=True,
    )
    
    dataset_type = Column(
        String(100),
        nullable=True,
        index=True,
    )
    
    column_names = Column(
        JSON,
        nullable=True,
    )
    data_types = Column(
        JSON,
        nullable=True,
    )
    
    memory_mb = Column(
        Float,
        default=0,
    )
    
    graph_processed = Column(
        Boolean,
        default=False,
    )
    
    entity_resolution_completed = Column(
        Boolean,
        default=False,
    )
    
    risk_scoring_completed = Column(
        Boolean,
        default=False,
    )
    investigation_ready = Column(
        Boolean,
        default=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )