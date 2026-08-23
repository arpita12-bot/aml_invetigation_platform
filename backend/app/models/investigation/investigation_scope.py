"""
==========================================================
AML Investigation Platform

Investigation Scope

Defines the boundary of an investigation.

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class InvestigationScope:
    """
    Defines which portion of the graph
    should be investigated.
    """

    entity_id: str

    entity_type: str = "Company"

    max_depth: int = 3

    include_transactions: bool = True

    include_pep: bool = True

    include_sanctions: bool = True

    include_devices: bool = False

    include_adverse_news: bool = True