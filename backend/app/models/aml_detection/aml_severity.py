"""
==========================================================
AML Investigation Platform

AML Severity

==========================================================
"""

from __future__ import annotations

from enum import Enum


class AMLSeverity(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"