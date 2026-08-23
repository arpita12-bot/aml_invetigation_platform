"""
==========================================================
AML Investigation Platform

Dataset Status Constants

==========================================================
"""

from enum import Enum


class UploadStatus(str, Enum):
    PENDING = "PENDING"
    UPLOADING = "UPLOADING"
    UPLOADED = "UPLOADED"
    FAILED = "FAILED"


class ValidationStatus(str, Enum):
    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    PASSED = "PASSED"
    FAILED = "FAILED"


class ProcessingStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"