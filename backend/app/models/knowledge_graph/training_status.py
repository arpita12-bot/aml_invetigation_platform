"""
==========================================================
AML Investigation Platform

Training Status

Represents the lifecycle of a Knowledge Graph
Embedding training job.

==========================================================
"""

from __future__ import annotations

from enum import Enum


class TrainingStatus(str, Enum):
    """
    Status of a model training job.
    """

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"