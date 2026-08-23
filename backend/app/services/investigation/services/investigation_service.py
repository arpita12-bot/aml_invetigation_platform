"""
==========================================================
AML Investigation Platform

Investigation Service

Responsibilities
----------------
✓ Execute AML investigation
✓ Coordinate evidence collection
✓ Map investigation results
✓ Return API response

This service orchestrates the investigation workflow.
It intentionally contains no graph algorithms,
Cypher queries, or repository logic.

==========================================================
"""

from __future__ import annotations

from app.api.investigation.schemas.investigation_response_dto import (
    InvestigationResponseDTO,
)

from app.models.investigation.investigation_request import (
    InvestigationRequest,
)

from app.services.investigation.evidence_collector import (
    EvidenceCollector,
)

from app.services.investigation.mappers.investigation_mapper import (
    InvestigationMapper,
)


class InvestigationService:
    """
    Executes an AML investigation.

    Workflow

        InvestigationRequest
                │
                ▼
        EvidenceCollector
                │
                ▼
        InvestigationContext
                │
                ▼
        InvestigationMapper
                │
                ▼
        InvestigationResponseDTO
    """

    def __init__(
        self,
        evidence_collector: EvidenceCollector,
    ) -> None:

        self._collector = evidence_collector

    # =====================================================
    # Public API
    # =====================================================

    def investigate(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponseDTO:
        """
        Execute an AML investigation.

        Parameters
        ----------
        request:
            Validated investigation request.

        Returns
        -------
        InvestigationResponseDTO
            Investigation response suitable for
            API serialization.
        """

        context = self._collector.collect(
            request=request,
        )

        return InvestigationMapper.map(
            context,
        )
        
    