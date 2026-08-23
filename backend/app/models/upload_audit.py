"""
==========================================================
AML Investigation Platform

Upload Audit Model

Responsibilities
----------------
✓ Track every upload attempt
✓ Store validation results
✓ Record processing metrics
✓ Capture errors and warnings
✓ Maintain audit history

==========================================================
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)

from app.database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

from app.core.constants import ProcessingStatus

class UploadAudit(Base):
    """
    Audit log for every dataset upload.
    """

    __tablename__ = "upload_audit"

    # ======================================================
    # Primary Key
    # ======================================================

    audit_id = Column(
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
        index=True,
    )

    # ======================================================
    # Upload Information
    # ======================================================

    upload_session_id = Column(
        String(100),
        nullable=False,
        index=True,
    )

    uploaded_by = Column(
        String(100),
        nullable=True,
    )

    uploaded_from_ip = Column(
        String(50),
        nullable=True,
    )

    # ======================================================
    # File Information
    # ======================================================

    original_filename = Column(
        String(255),
        nullable=False,
    )

    table_name = Column(
        String(255),
        nullable=False,
    )

    file_hash = Column(
        String(128),
        nullable=False,
    )

    # ======================================================
    # Processing Statistics
    # ======================================================

    total_rows = Column(
        Integer,
        default=0,
    )

    inserted_rows = Column(
        Integer,
        default=0,
    )

    updated_rows = Column(
        Integer,
        default=0,
    )

    skipped_rows = Column(
        Integer,
        default=0,
    )

    duplicate_rows = Column(
        Integer,
        default=0,
    )

    rejected_rows = Column(
        Integer,
        default=0,
    )

    # ======================================================
    # Validation Results
    # ======================================================

    validation_passed = Column(
        Boolean,
        default=False,
    )

    validation_errors = Column(
        JSON,
        nullable=True,
    )

    validation_warnings = Column(
        JSON,
        nullable=True,
    )

    # ======================================================
    # Processing Information
    # ======================================================

    processing_status = Column(
    Enum(ProcessingStatus, name="processing_status_enum"),
    default=ProcessingStatus.PENDING,
    nullable=False,
    )

    processing_stage = Column(
        String(100),
        nullable=True,
    )

    processing_time_seconds = Column(
        Float,
        default=0.0,
    )

    # ======================================================
    # Error Information
    # ======================================================

    error_code = Column(
        String(100),
        nullable=True,
    )

    error_message = Column(
        Text,
        nullable=True,
    )

    stack_trace = Column(
        Text,
        nullable=True,
    )

    # ======================================================
    # Data Quality Metrics
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
    # Performance Metrics
    # ======================================================

    upload_size_mb = Column(
        Float,
        default=0.0,
    )

    rows_per_second = Column(
        Float,
        default=0.0,
    )

    # ======================================================
    # Additional Metadata
    # ======================================================

    remarks = Column(
        Text,
        nullable=True,
    )

    additional_metadata = Column(
        JSON,
        nullable=True,
    )

    completed_at = Column(
        DateTime,
        nullable=True,
    )
    
    # ======================================================
    # Relationship
    # ======================================================

    dataset = relationship(
        "DatasetRegistry",
        back_populates="upload_audits",
        lazy="selectin",
    )