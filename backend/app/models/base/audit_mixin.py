"""
==========================================================
AML Investigation Platform

Audit Mixin

==========================================================
"""

from __future__ import annotations

from dataclasses import field


class AuditMixin:

    created_by: str | None = field(
        default=None
    )

    updated_by: str | None = field(
        default=None
    )