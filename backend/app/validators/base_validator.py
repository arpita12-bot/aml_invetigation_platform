"""
==========================================================
AML Investigation Platform

Base Validator

Responsibilities
----------------
✓ Base class for all validators
✓ Common validation interface
✓ Validation result model
✓ Shared helper methods
✓ Validator execution priority

==========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from app.validators.column_detector import DetectedColumns


# ==========================================================
# Validation Result
# ==========================================================


@dataclass
class ValidationResult:
    """
    Standard validation result returned by every validator.
    """

    validator_name: str

    passed: bool = True

    errors: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    statistics: dict[str, Any] = field(default_factory=dict)

    # NEW
    execution_time_ms: float = 0.0

# ==========================================================
# Base Validator
# ==========================================================


class BaseValidator(ABC):
    """
    Base validator inherited by every AML validator.
    """

    # ----------------------------------------------
    # Validator Metadata
    # ----------------------------------------------

    name: str = "Base Validator"

    priority: int = 100

    supported_columns: list[str] = []

    # ----------------------------------------------
    # Validation Interface
    # ----------------------------------------------

    @abstractmethod
    def validate(
        self,
        dataframe: pd.DataFrame,
        detected_columns: DetectedColumns,
    ) -> ValidationResult:
        """
        Execute validator.

        Must be implemented by child validators.
        """
        raise NotImplementedError

    # ----------------------------------------------
    # Result Helpers
    # ----------------------------------------------

    def create_result(self) -> ValidationResult:

        return ValidationResult(
            validator_name=self.name
        )

    def add_error(
        self,
        result: ValidationResult,
        message: str,
    ) -> None:

        result.passed = False

        result.errors.append(message)

    def add_warning(
        self,
        result: ValidationResult,
        message: str,
    ) -> None:

        result.warnings.append(message)

    def add_statistic(
        self,
        result: ValidationResult,
        key: str,
        value: Any,
    ) -> None:

        result.statistics[key] = value

    # ----------------------------------------------
    # Column Helpers
    # ----------------------------------------------

    def matching_columns(
        self,
        detected_columns: DetectedColumns,
    ) -> list[str]:
        """
        Return matching dataframe columns for
        this validator.
        """

        matches: list[str] = []

        for value in vars(detected_columns).values():

            if not isinstance(value, list):
                continue

            for column in value:

                if column.lower() in self.supported_columns:
                    matches.append(column)

        return matches

    def has_supported_columns(
        self,
        detected_columns: DetectedColumns,
    ) -> bool:

        return len(
            self.matching_columns(
                detected_columns
            )
        ) > 0

    # ----------------------------------------------
    # Sorting Support
    # ----------------------------------------------

    def __lt__(
        self,
        other: "BaseValidator",
    ) -> bool:

        return self.priority < other.priority