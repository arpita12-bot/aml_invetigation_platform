"""
==========================================================
AML Investigation Platform

File Utility Functions

Responsibilities
----------------
✓ Validate uploaded files
✓ Validate file extension
✓ Validate file size
✓ Create upload directories
✓ Generate unique filenames
✓ Save uploaded files
✓ Generate file metadata
✓ Delete temporary files
✓ MIME type detection

==========================================================
"""

from __future__ import annotations

import shutil
import uuid
from datetime import datetime
from pathlib import Path

import magic
from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import (
    EmptyFileError,
    FileTooLargeError,
    UnsupportedFileTypeError,
)
from app.utils.hash_utils import calculate_file_hash


# ==========================================================
# Upload Directory
# ==========================================================

def create_upload_directory() -> Path:
    """
    Create upload directory if it doesn't exist.
    """

    upload_path = settings.upload_path

    upload_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return upload_path


# ==========================================================
# File Extension
# ==========================================================

def get_file_extension(filename: str) -> str:
    """
    Return lowercase file extension.
    """

    return Path(filename).suffix.lower()


# ==========================================================
# Validate Extension
# ==========================================================

def validate_file_extension(filename: str) -> None:
    """
    Validate uploaded file extension.
    """

    extension = get_file_extension(filename)

    if extension not in settings.allowed_extensions:
        raise UnsupportedFileTypeError(
            f"Unsupported file type: {extension}"
        )


# ==========================================================
# Validate File Size
# ==========================================================

def validate_file_size(file_size: int) -> None:
    """
    Validate uploaded file size.
    """

    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if file_size <= 0:
        raise EmptyFileError(
            "Uploaded file is empty."
        )

    if file_size > max_size:
        raise FileTooLargeError(
            f"Maximum allowed size is "
            f"{settings.MAX_UPLOAD_SIZE_MB} MB."
        )


# ==========================================================
# MIME Type
# ==========================================================

def detect_mime_type(file_path: str | Path) -> str:
    """
    Detect MIME type.
    """

    return magic.from_file(
        str(file_path),
        mime=True,
    )


# ==========================================================
# Unique Filename
# ==========================================================

def generate_unique_filename(
    original_filename: str,
) -> str:
    """
    Generate unique filename.
    """

    extension = get_file_extension(original_filename)

    timestamp = datetime.utcnow().strftime(
        "%Y%m%d_%H%M%S"
    )

    unique = uuid.uuid4().hex[:8]

    return (
        f"{timestamp}_"
        f"{unique}"
        f"{extension}"
    )


# ==========================================================
# Save Uploaded File
# ==========================================================

def save_uploaded_file(
    upload_file: UploadFile,
) -> Path:
    """
    Save uploaded file to disk.
    """

    create_upload_directory()

    filename = generate_unique_filename(
        upload_file.filename
    )

    destination = (
        settings.upload_path / filename
    )

    with destination.open("wb") as buffer:
        shutil.copyfileobj(
            upload_file.file,
            buffer,
        )

    return destination


# ==========================================================
# Validate Uploaded File
# ==========================================================

def validate_uploaded_file(
    upload_file: UploadFile,
) -> None:
    """
    Validate uploaded file.
    """

    validate_file_extension(
        upload_file.filename
    )


# ==========================================================
# File Metadata
# ==========================================================

def get_file_metadata(
    file_path: str | Path,
) -> dict:
    """
    Generate file metadata.
    """

    path = Path(file_path)

    size = path.stat().st_size

    return {

        "filename": path.name,

        "extension": path.suffix.lower(),

        "size_bytes": size,

        "size_mb": round(
            size / (1024 * 1024),
            2,
        ),

        "mime_type": detect_mime_type(path),

        "file_hash": calculate_file_hash(path),

        "created_at": datetime.utcnow(),
    }


# ==========================================================
# Delete File
# ==========================================================

def delete_file(
    file_path: str | Path,
) -> None:
    """
    Delete file if it exists.
    """

    path = Path(file_path)

    if path.exists():
        path.unlink()


# ==========================================================
# Delete Directory
# ==========================================================

def delete_directory(
    directory: str | Path,
) -> None:
    """
    Delete directory recursively.
    """

    directory = Path(directory)

    if directory.exists():
        shutil.rmtree(directory)