from dataclasses import dataclass, field


@dataclass(slots=True)
class ValidationSummary:

    quality_score: float

    execution_time_ms: float

    validator_results: list = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    def to_dict(self):

        return {

            "quality_score": self.quality_score,

            "execution_time_ms": self.execution_time_ms,

            "validator_results": self.validator_results,

            "errors": self.errors,

            "warnings": self.warnings,

        }