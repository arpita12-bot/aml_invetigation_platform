from __future__ import annotations

import time
import traceback

import pandas as pd

from app.core.validation_settings import ENABLED_VALIDATORS

from app.validators.base_validator import (
    ValidationResult,
    ValidationSummary,
)

from app.validators.column_detector import ColumnDetector
from app.validators.validator_registry import ValidatorRegistry

# ==========================================================
# AML Validation Service
# ==========================================================


class AMLValidationService:

    """
    Enterprise validation engine.
    """
    # ==========================================
    # Validator Weights
    # ==========================================

    VALIDATOR_WEIGHTS = {

        "Customer Validator": 20,

        "Transaction Validator": 25,

        "Company Validator": 15,

        "Risk Validator": 15,

        "Email Validator": 5,

        "Phone Validator": 5,

        "Date Validator": 5,

        "Amount Validator": 5,

        "Currency Validator": 3,

        "Country Validator": 2,

        "Account Validator": 5,
    }

    def __init__(self):

        self.validators = [

            validator

            for validator in ValidatorRegistry.get_validators()

            if ENABLED_VALIDATORS.get(
                validator.name,
                True,
            )

        ]
    
    @classmethod
    def _calculate_quality_score(
        cls,
        results: list[ValidationResult],
    ) -> float:

        score = 100.0

        for result in results:

            weight = cls.VALIDATOR_WEIGHTS.get(
                result.validator_name,
                1,
            )

            score -= (
                len(result.errors)
                * weight
                * 0.5
            )

            score -= (
                len(result.warnings)
                * weight
                * 0.1
            )

        return max(
            round(score, 2),
            0,
        )
        
        
    @staticmethod
    def dataset_grade(
        score: float,
    ) -> str:

        if score >= 95:
            return "A+"

        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        if score >= 60:
            return "D"

        return "F"    
        
    
    @staticmethod
    def _merge_statistics(
        results: list[ValidationResult],
    ) -> dict:

        statistics = {}

        for result in results:

            statistics[result.validator_name] = (
                result.statistics
            )

        return statistics
    
    @staticmethod
    def _count_errors(
        results,
    ):

        return sum(
            len(r.errors)
            for r in results
        )


    @staticmethod
    def _count_warnings(
        results,
    ):

        return sum(
            len(r.warnings)
            for r in results
        )
    
    @staticmethod
    def validator_rank(
        summary: ValidationSummary,
    ):

        return sorted(

            summary.validator_results,

            key=lambda x: len(x.errors),

            reverse=True,

        )
    # ======================================================
    # Main Validation Engine
    # ======================================================

    def validate(
        self,
        dataframe: pd.DataFrame,
        dataset_name: str | None = None,
        ) -> ValidationSummary:
        """
        Validate an uploaded dataset.

        Parameters
        ----------
        dataframe : pd.DataFrame
            Dataset to validate.

        dataset_name : str
            Optional dataset name.

        Returns
        -------
        ValidationSummary
        """

        start_time = time.perf_counter()
        metadata["grade"] = self.dataset_grade(
            quality_score
        )
        # ---------------------------------------------
        # Detect Dataset Columns
        # ---------------------------------------------

        detected_columns = ColumnDetector.detect(
            dataframe
        )

        validation_results: list[ValidationResult] = []

        # ---------------------------------------------
        # Execute Validators
        # ---------------------------------------------

        for validator in self.validators:

            try:

                validator_start = time.perf_counter()

                result = validator.validate(
                    dataframe=dataframe,
                    detected_columns=detected_columns,
                )

                result.execution_time_ms = round(
                    (
                        time.perf_counter()
                        - validator_start
                    ) * 1000,
                    2,
                )

                validation_results.append(result)

            except Exception as ex:

                error_result = ValidationResult(
                    validator_name=validator.name,
                    passed=False,
                )

                error_result.errors.append(
                    str(ex)
                )

                error_result.statistics[
                    "traceback"
                ] = traceback.format_exc()

                validation_results.append(
                    error_result
                )

        # ---------------------------------------------
        # Aggregate Results
        # ---------------------------------------------

        total_errors = self._count_errors(
            validation_results
        )

        total_warnings = self._count_warnings(
            validation_results
        )

        quality_score = (
            self._calculate_quality_score(
                validation_results
            )
        )

        execution_time = (
            time.perf_counter()
            - start_time
        )

        statistics = self._merge_statistics(
            validation_results
        )
                
        # ---------------------------------------------
        # Metadata
        # ---------------------------------------------

        metadata = {

            "dataset_name": dataset_name,

            "rows": len(dataframe),

            "columns": len(dataframe.columns),

            "column_names": list(dataframe.columns),

            "validator_count": len(self.validators),

        }
        
        metadata["grade"] = self.dataset_grade(
            quality_score
        )

        passed = total_errors == 0
        
        # ---------------------------------------------
        # Return Summary
        # ---------------------------------------------

        return ValidationSummary(

            passed=passed,

            overall_score=quality_score,

            detected_columns=detected_columns,

            validator_results=validation_results,

            total_errors=total_errors,

            total_warnings=total_warnings,

            execution_time_seconds=round(
                execution_time,
                4,
            ),

            statistics=statistics,

            metadata=metadata,

        )
        
    # ======================================================
    # Failed Validators
    # ======================================================

    @staticmethod
    def get_failed_validators(
        summary: ValidationSummary,
    ) -> list[str]:

        return [

            result.validator_name

            for result in summary.validator_results

            if not result.passed

        ]
            
    # ======================================================
    # Collect Errors
    # ======================================================

    @staticmethod
    def get_errors(
        summary: ValidationSummary,
    ) -> list[str]:

        errors = []

        for result in summary.validator_results:

            for error in result.errors:

                errors.append(

                    f"[{result.validator_name}] {error}"

                )

        return errors
    
        
    # ======================================================
    # Collect Warnings
    # ======================================================

    @staticmethod
    def get_warnings(
        summary: ValidationSummary,
    ) -> list[str]:

        warnings = []

        for result in summary.validator_results:

            for warning in result.warnings:

                warnings.append(

                    f"[{result.validator_name}] {warning}"

                )

        return warnings
    
        
    # ======================================================
    # Validation Report
    # ======================================================

    @staticmethod
    def generate_report(
        summary: ValidationSummary,
    ) -> dict:

        return {

            "passed": summary.passed,

            "quality_score": summary.overall_score,

            "total_errors": summary.total_errors,

            "total_warnings": summary.total_warnings,

            "execution_time_seconds":
                summary.execution_time_seconds,

            "metadata":
                summary.metadata,

            "failed_validators":

                AMLValidationService.get_failed_validators(
                    summary
                ),

            "errors":

                AMLValidationService.get_errors(
                    summary
                ),

            "warnings":

                AMLValidationService.get_warnings(
                    summary
                ),

            "statistics":

                summary.statistics,
                
            "validators": [
                {
                    "name": result.validator_name,
                    "passed": result.passed,
                    "errors": len(result.errors),
                    "warnings": len(result.warnings),
                    "execution_time_ms": result.execution_time_ms,
                }
                for result in summary.validator_results
            ]

        }
    

    # ======================================================
    # Dashboard Summary
    # ======================================================

    @staticmethod
    def dashboard(
        summary: ValidationSummary,
    ) -> dict:

        return {

            "quality_score": summary.overall_score,

            "grade": summary.metadata.get(
                "grade",
                "N/A",
            ),

            "errors": summary.total_errors,

            "warnings": summary.total_warnings,

            "execution_time": summary.execution_time_seconds,

            "validators": [

                {

                    "name": result.validator_name,

                    "passed": result.passed,

                    "errors": len(result.errors),

                    "warnings": len(result.warnings),

                }

                for result in summary.validator_results

            ],

        }
        
        
    # ======================================================
    # Console Summary
    # ======================================================

    @staticmethod
    def print_summary(
        summary: ValidationSummary,
    ) -> None:

        print("\n")

        print("=" * 70)

        print("AML VALIDATION SUMMARY")

        print("=" * 70)

        print(f"Passed              : {summary.passed}")

        print(f"Quality Score       : {summary.overall_score}")

        print(f"Errors              : {summary.total_errors}")

        print(f"Warnings            : {summary.total_warnings}")

        print(
            f"Execution Time (s)  : "
            f"{summary.execution_time_seconds}"
        )

        print("=" * 70)

        print(
            f"{'Validator':<30}"
            f"{'Status':<10}"
            f"{'Errors':<10}"
            f"{'Warnings':<10}"
            f"{'Time (ms)':>12}"
        )

        print("-" * 75)

        for result in summary.validator_results:

            status = "PASS" if result.passed else "FAIL"

            print(
                f"{result.validator_name:<30}"
                f"{status:<10}"
                f"{len(result.errors):<10}"
                f"{len(result.warnings):<10}"
                f"{result.execution_time_ms:>12.2f}"
            )

        print("=" * 70)
        
    # ======================================================
    # Dataset Profile
    # ======================================================

    @staticmethod
    def profile_dataset(
        dataframe: pd.DataFrame,
    ) -> dict:

        return {

            "rows": len(dataframe),

            "columns": len(dataframe.columns),

            "missing_values":

                dataframe.isna().sum().sum(),

            "duplicate_rows":

                dataframe.duplicated().sum(),

            "memory_mb":

                round(

                    dataframe.memory_usage(
                        deep=True
                    ).sum()

                    / 1024

                    / 1024,

                    2,

                ),

        }
        
