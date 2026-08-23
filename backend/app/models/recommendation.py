"""
==========================================================
AML Investigation Platform

Investigation Recommendation

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Recommendation:

    priority: int

    category: str

    title: str

    description: str

    mandatory: bool = False