"""
==========================================================
AML Investigation Platform

Custom Application Exceptions

Responsibilities
----------------
✓ Upload Exceptions
✓ Validation Exceptions
✓ Database Exceptions
✓ Graph Exceptions
✓ ML Exceptions

==========================================================
"""


class AMLPlatformException(Exception):
    """
    Base exception for the AML platform.
    """

    def __init__(self, message: str):
        super().__init__(message)


# ==========================================================
# File Exceptions
# ==========================================================

class UnsupportedFileTypeError(AMLPlatformException):
    """Raised when an unsupported file type is uploaded."""
    pass


class FileTooLargeError(AMLPlatformException):
    """Raised when the uploaded file exceeds the maximum size."""
    pass


class EmptyFileError(AMLPlatformException):
    """Raised when the uploaded file contains no data."""
    pass


class DuplicateDatasetError(AMLPlatformException):
    """Raised when the uploaded dataset already exists."""
    pass


# ==========================================================
# Validation Exceptions
# ==========================================================

class DatasetValidationError(AMLPlatformException):
    """Raised when dataset validation fails."""
    pass


class SchemaValidationError(AMLPlatformException):
    """Raised when schema validation fails."""
    pass


class DataQualityError(AMLPlatformException):
    """Raised when the dataset does not satisfy quality rules."""
    pass


# ==========================================================
# Database Exceptions
# ==========================================================

class DatabaseConnectionError(AMLPlatformException):
    """Raised when the database is unavailable."""
    pass


class DynamicTableCreationError(AMLPlatformException):
    """Raised when dynamic table creation fails."""
    pass


# ==========================================================
# Knowledge Graph Exceptions
# ==========================================================

class GraphBuildError(AMLPlatformException):
    """Raised when graph generation fails."""
    pass


class EntityResolutionError(AMLPlatformException):
    """Raised when entity resolution fails."""
    pass


# ==========================================================
# Machine Learning Exceptions
# ==========================================================

class EmbeddingTrainingError(AMLPlatformException):
    """Raised when TransE / RotatE training fails."""
    pass


class LinkPredictionError(AMLPlatformException):
    """Raised when link prediction fails."""
    pass