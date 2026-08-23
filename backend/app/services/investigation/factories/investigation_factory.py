"""
==========================================================
AML Investigation Platform

Investigation Factory

Responsibilities
----------------
✓ Build InvestigationScope
✓ Build InvestigationRequest
✓ Apply default investigation settings
✓ Validate investigation request
✓ Return validated domain model

The factory converts API/controller input into
validated domain objects. No business logic or
database access should exist here.

==========================================================
"""

from __future__ import annotations

from app.models.investigation.investigation_request import (
    InvestigationRequest,
)
from app.models.investigation.investigation_scope import (
    InvestigationScope,
)
from app.services.investigation.validators.investigation_validator import (
    InvestigationValidator,
)


class InvestigationFactory:
    """
    Factory responsible for constructing validated
    investigation domain models.
    """

    @staticmethod
    def create(
        *,
        entity_id: str,
        entity_type: str,
        analyst: str,
        case_id: str,
        max_depth: int = 3,
        include_transactions: bool = True,
        include_pep: bool = True,
        include_sanctions: bool = True,
        include_devices: bool = False,
        include_adverse_news: bool = True,
    ) -> InvestigationRequest:
        """
        Create and validate an InvestigationRequest.

        Parameters
        ----------
        entity_id:
            Root entity identifier.

        entity_type:
            Type of entity (Customer, Company, Account, etc.).

        analyst:
            Analyst performing the investigation.

        case_id:
            Investigation case identifier.

        max_depth:
            Maximum graph traversal depth.

        include_transactions:
            Include transaction relationships.

        include_pep:
            Include politically exposed persons.

        include_sanctions:
            Include sanctions.

        include_devices:
            Include linked devices.

        include_adverse_news:
            Include adverse news entities.

        Returns
        -------
        InvestigationRequest
            Fully validated investigation request.
        """

        scope = InvestigationScope(
            entity_id=entity_id,
            entity_type=entity_type,
            max_depth=max_depth,
            include_transactions=include_transactions,
            include_pep=include_pep,
            include_sanctions=include_sanctions,
            include_devices=include_devices,
            include_adverse_news=include_adverse_news,
        )

        request = InvestigationRequest(
            case_id=case_id,
            analyst=analyst,
            scope=scope,
        )

        InvestigationValidator.validate_request(request)

        return request