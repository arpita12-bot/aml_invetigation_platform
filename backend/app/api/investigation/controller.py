"""
==========================================================
AML Investigation Platform

Investigation Controller

Responsibilities
----------------
✓ Accept API requests
✓ Build InvestigationRequest
✓ Execute investigation
✓ Return investigation response

==========================================================
"""

from __future__ import annotations

from app.api.investigation.schemas.investigation_request_dto import (
    InvestigationRequestDTO,
)

from app.api.investigation.schemas.investigation_response_dto import (
    InvestigationResponseDTO,
)

from app.services.investigation.factories.investigation_factory import (
    InvestigationFactory,
)

from app.services.investigation.services.investigation_service import (
    InvestigationService,
)


class InvestigationController:
    """
    Thin application controller responsible for
    orchestrating investigation execution.
    """

    def __init__(
        self,
        service: InvestigationService,
    ) -> None:

        self._service = service

    # =====================================================
    # Public API
    # =====================================================

    def investigate(
        self,
        dto: InvestigationRequestDTO,
    ) -> InvestigationResponseDTO:
        """
        Execute AML investigation.
        """

        request = InvestigationFactory.create(

            entity_id=dto.entity_id,

            entity_type=dto.entity_type,

            analyst=dto.analyst,

            case_id=dto.case_id,

            max_depth=dto.max_depth,

            include_transactions=dto.include_transactions,

            include_pep=dto.include_pep,

            include_sanctions=dto.include_sanctions,

            include_devices=dto.include_devices,

            include_adverse_news=dto.include_adverse_news,

        )

        return self._service.investigate(request)