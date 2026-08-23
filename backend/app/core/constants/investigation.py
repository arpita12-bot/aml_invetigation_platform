"""
==========================================================
AML Investigation Platform

Investigation Constants

Responsibilities
----------------
✓ Investigation depth limits
✓ Investigation defaults
✓ Investigation configuration

==========================================================
"""

from __future__ import annotations

MIN_INVESTIGATION_DEPTH = 1

MAX_INVESTIGATION_DEPTH = 10

DEFAULT_INVESTIGATION_DEPTH = 3

__all__ = [
    "MIN_INVESTIGATION_DEPTH",
    "MAX_INVESTIGATION_DEPTH",
    "DEFAULT_INVESTIGATION_DEPTH",
]