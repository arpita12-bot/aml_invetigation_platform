"""
==========================================================
AML Investigation Platform

Investigation Validator

Responsibilities
----------------
✓ Validate investigation requests
✓ Validate investigation scope
✓ Enforce business rules
✓ Raise domain validation exceptions

==========================================================
"""

from __future__ import annotations

from app.core.constants import (
    SUPPORTED_ENTITY_TYPES,
)

from app.models.investigation.investigation_request import (
    InvestigationRequest,
)

from app.models.investigation.investigation_scope import (
    InvestigationScope,
)

from app.services.investigation.exceptions import (
    InvestigationValidationException,
)

from app.core.constants import (
    MAX_INVESTIGATION_DEPTH,
    MIN_INVESTIGATION_DEPTH,
)

class InvestigationValidator:
    """
    Central validator for all investigation requests.
    """

    MIN_DEPTH = MIN_INVESTIGATION_DEPTH

    MAX_DEPTH = MAX_INVESTIGATION_DEPTH

    SUPPORTED_ENTITY_TYPES = SUPPORTED_ENTITY_TYPES
    
    @classmethod
    def validate_request(
        cls,
        request: InvestigationRequest,
    ) -> None:
        """
        Validate a complete investigation request.
        """

        if request is None:
            raise InvestigationValidationException(
                "Investigation request cannot be None."
            )

        cls.validate_case_id(request.case_id)
        cls.validate_analyst(request.analyst)
        cls.validate_scope(request.scope)

    @classmethod
    def validate_scope(
        cls,
        scope: InvestigationScope,
    ) -> None:
        """
        Validate investigation scope.
        """

        if scope is None:
            raise InvestigationValidationException(
                "Investigation scope cannot be None."
            )

        cls.validate_entity_id(scope.entity_id)
        cls.validate_entity_type(scope.entity_type)
        cls.validate_depth(scope.max_depth)

    @staticmethod
    def validate_case_id(
        case_id: str,
    ) -> None:
        """
        Validate investigation case ID.
        """

        if not case_id or not case_id.strip():
            raise InvestigationValidationException(
                "Case ID is required."
            )

    @staticmethod
    def validate_analyst(
        analyst: str,
    ) -> None:
        """
        Validate analyst name.
        """

        if not analyst or not analyst.strip():
            raise InvestigationValidationException(
                "Analyst name is required."
            )

    @staticmethod
    def validate_entity_id(
        entity_id: str,
    ) -> None:
        """
        Validate investigation root entity ID.
        """

        if not entity_id or not entity_id.strip():
            raise InvestigationValidationException(
                "Entity ID is required."
            )

    @classmethod
    def validate_entity_type(
        cls,
        entity_type: str,
    ) -> None:
        """
        Validate investigation entity type.
        """

        if not entity_type:
            raise InvestigationValidationException(
                "Entity type is required."
            )

        entity_type = entity_type.strip().upper()

        if entity_type not in cls.SUPPORTED_ENTITY_TYPES:
            raise InvestigationValidationException(
                f"Unsupported entity type: {entity_type}"
            )

    @classmethod
    def validate_depth(
        cls,
        depth: int,
    ) -> None:
        """
        Validate investigation traversal depth.
        """

        if depth < cls.MIN_DEPTH:
            raise InvestigationValidationException(
                f"Maximum depth must be >= {cls.MIN_DEPTH}."
            )

        if depth > cls.MAX_DEPTH:
            raise InvestigationValidationException(
                f"Maximum depth must be <= {cls.MAX_DEPTH}."
            )