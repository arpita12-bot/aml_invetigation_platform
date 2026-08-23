"""
==========================================================
AML Investigation Platform

Serialization Mixin

==========================================================
"""

from __future__ import annotations

from dataclasses import asdict


class SerializationMixin:
    """
    Provides dictionary serialization
    for dataclass-based models.
    """

    def to_dict(self) -> dict:

        return asdict(self)