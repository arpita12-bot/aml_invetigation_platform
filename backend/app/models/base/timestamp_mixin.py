"""
==========================================================
AML Investigation Platform

Timestamp Mixin

==========================================================
"""

from __future__ import annotations

from dataclasses import field
from datetime import datetime


class TimestampMixin:

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )