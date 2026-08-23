"""
==========================================================
AML Investigation Platform

Enterprise Confidence Engine

Responsibilities
----------------
✓ Convert similarity into confidence
✓ Apply AML business rules
✓ Decide AUTO_MATCH / MANUAL_REVIEW / NO_MATCH
✓ Produce explainable decisions
✓ Generate audit-ready results
✓ Support enterprise diagnostics
==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Generator, Iterable, List, Optional

from app.entity_resolution.services.similarity_engine import (
    SimilarityResult,
)


# ==========================================================
# Decision Enum
# ==========================================================

class ConfidenceDecision(str, Enum):
    """
    Final entity resolution decision.
    """

    AUTO_MATCH = "AUTO_MATCH"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    NO_MATCH = "NO_MATCH"


# ==========================================================
# Review Priority
# ==========================================================

class ReviewPriority(str, Enum):
    """
    Manual review priority.
    """

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"


# ==========================================================
# Confidence Result
# ==========================================================

@dataclass(slots=True)
class ConfidenceResult:
    """
    Final confidence evaluation.
    """

    left_index: int

    right_index: int

    similarity_score: float

    confidence_score: float

    decision: ConfidenceDecision

    priority: ReviewPriority

    requires_review: bool

    explanation: List[str] = field(default_factory=list)

    rule_scores: Dict[str, float] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Configuration
# ==========================================================

@dataclass(slots=True)
class ConfidenceConfiguration:
    """
    Confidence engine configuration.
    """

    auto_match_threshold: float = 0.95

    manual_review_threshold: float = 0.80

    reject_threshold: float = 0.50

    critical_field_bonus: float = 0.03

    critical_field_penalty: float = 0.05

    phone_bonus: float = 0.02

    email_bonus: float = 0.02

    dob_bonus: float = 0.02

    company_bonus: float = 0.01

    country_penalty: float = 0.03

    risk_penalty: float = 0.02

    normalize_score: bool = True


# ==========================================================
# Runtime Statistics
# ==========================================================

@dataclass(slots=True)
class ConfidenceStatistics:
    """
    Runtime statistics.
    """

    processed: int = 0

    auto_matches: int = 0

    manual_reviews: int = 0

    rejected: int = 0

    cumulative_score: float = 0.0

    average_confidence: float = 0.0


# ==========================================================
# Confidence Engine
# ==========================================================

class ConfidenceEngine:
    """
    Enterprise AML Confidence Engine.

    Converts SimilarityResult into
    business confidence decisions.
    """

    def __init__(
        self,
        config: Optional[
            ConfidenceConfiguration
        ] = None,
    ) -> None:

        self.config = (
            config
            or
            ConfidenceConfiguration()
        )

        self.statistics = (
            ConfidenceStatistics()
        )

        self.validate_configuration()

    # -----------------------------------------------------
    # Configuration Validation
    # -----------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate thresholds.
        """

        cfg = self.config

        if not (
            cfg.auto_match_threshold
            >
            cfg.manual_review_threshold
            >
            cfg.reject_threshold
        ):
            raise ValueError(
                "Invalid confidence thresholds."
            )

    # -----------------------------------------------------
    # Reset
    # -----------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset runtime statistics.
        """

        self.statistics = (
            ConfidenceStatistics()
        )

    # -----------------------------------------------------
    # Normalize
    # -----------------------------------------------------

    def normalize(
        self,
        score: float,
    ) -> float:
        """
        Clamp score between 0 and 1.
        """

        score = max(
            0.0,
            min(
                1.0,
                score,
            ),
        )

        return round(
            score,
            4,
        )

    # -----------------------------------------------------
    # Decision Helpers
    # -----------------------------------------------------

    def is_auto_match(
        self,
        score: float,
    ) -> bool:

        return (
            score
            >=
            self.config.auto_match_threshold
        )

    def is_manual_review(
        self,
        score: float,
    ) -> bool:

        return (

            self.config.manual_review_threshold

            <=

            score

            <

            self.config.auto_match_threshold

        )

    def is_rejected(
        self,
        score: float,
    ) -> bool:

        return (
            score
            <
            self.config.manual_review_threshold
        )

    # -----------------------------------------------------
    # Confidence Level
    # -----------------------------------------------------

    def confidence_level(
        self,
        score: float,
    ) -> str:

        if score >= 0.95:
            return "VERY_HIGH"

        if score >= 0.90:
            return "HIGH"

        if score >= 0.80:
            return "MEDIUM"

        if score >= 0.60:
            return "LOW"

        return "VERY_LOW"

    # -----------------------------------------------------
    # Runtime Statistics
    # -----------------------------------------------------

    def update_statistics(
        self,
        result: ConfidenceResult,
    ) -> None:

        stats = self.statistics

        stats.processed += 1

        stats.cumulative_score += (
            result.confidence_score
        )

        stats.average_confidence = round(
            stats.cumulative_score
            /
            stats.processed,
            4,
        )

        if (
            result.decision
            ==
            ConfidenceDecision.AUTO_MATCH
        ):
            stats.auto_matches += 1

        elif (
            result.decision
            ==
            ConfidenceDecision.MANUAL_REVIEW
        ):
            stats.manual_reviews += 1

        else:
            stats.rejected += 1
            
        # -----------------------------------------------------
    # Critical Field Match
    # -----------------------------------------------------

    def critical_field_match(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, bool]:
        """
        Evaluate critical AML identity fields.
        """

        return {
            "name": similarity.name_score >= 0.90,
            "dob": similarity.dob_score == 1.0,
            "phone": similarity.phone_score == 1.0,
            "email": similarity.email_score == 1.0,
            "address": similarity.address_score >= 0.90,
            "company": similarity.company_score >= 0.90,
            "country": similarity.country_score == 1.0,
        }

    # -----------------------------------------------------
    # Rule Bonus
    # -----------------------------------------------------

    def rule_bonus(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, float]:
        """
        Positive confidence adjustments.
        """

        cfg = self.config

        bonus: Dict[str, float] = {}

        if similarity.phone_score == 1.0:
            bonus["phone"] = cfg.phone_bonus

        if similarity.email_score == 1.0:
            bonus["email"] = cfg.email_bonus

        if similarity.dob_score == 1.0:
            bonus["dob"] = cfg.dob_bonus

        if similarity.company_score >= 0.90:
            bonus["company"] = cfg.company_bonus

        return bonus

    # -----------------------------------------------------
    # Rule Penalty
    # -----------------------------------------------------

    def rule_penalty(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, float]:
        """
        Negative confidence adjustments.
        """

        cfg = self.config

        penalty: Dict[str, float] = {}

        if (
            0.0
            <
            similarity.dob_score
            <
            1.0
        ):
            penalty["dob"] = (
                cfg.critical_field_penalty
            )

        if (
            0.0
            <
            similarity.country_score
            <
            1.0
        ):
            penalty["country"] = (
                cfg.country_penalty
            )

        if (
            0.0
            <
            similarity.risk_level_score
            <
            1.0
        ):
            penalty["risk"] = (
                cfg.risk_penalty
            )

        return penalty

    # -----------------------------------------------------
    # Rule Score
    # -----------------------------------------------------

    def rule_score(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, float]:
        """
        Combined business rule score.
        """

        scores: Dict[str, float] = {}

        scores.update(
            self.rule_bonus(
                similarity,
            )
        )

        for key, value in self.rule_penalty(
            similarity,
        ).items():

            scores[key] = -value

        return scores

    # -----------------------------------------------------
    # Rule Adjustment
    # -----------------------------------------------------

    def rule_adjustment(
        self,
        similarity: SimilarityResult,
    ) -> float:
        """
        Net confidence adjustment.
        """

        adjustment = 0.0

        for value in self.rule_bonus(
            similarity,
        ).values():

            adjustment += value

        for value in self.rule_penalty(
            similarity,
        ).values():

            adjustment -= value

        return round(
            adjustment,
            4,
        )

    # -----------------------------------------------------
    # Critical Match Count
    # -----------------------------------------------------

    def critical_match_count(
        self,
        similarity: SimilarityResult,
    ) -> int:
        """
        Number of matched critical fields.
        """

        return sum(
            self.critical_field_match(
                similarity,
            ).values()
        )

    # -----------------------------------------------------
    # Critical Match Ratio
    # -----------------------------------------------------

    def critical_match_ratio(
        self,
        similarity: SimilarityResult,
    ) -> float:
        """
        Percentage of matched critical fields.
        """

        matches = self.critical_match_count(
            similarity,
        )

        total = len(
            self.critical_field_match(
                similarity,
            )
        )

        if total == 0:
            return 0.0

        return round(
            matches / total,
            4,
        )

    # -----------------------------------------------------
    # Rule Summary
    # -----------------------------------------------------

    def rule_summary(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, Any]:
        """
        AML business rule summary.
        """

        return {

            "critical_fields":
                self.critical_field_match(
                    similarity,
                ),

            "bonus":
                self.rule_bonus(
                    similarity,
                ),

            "penalty":
                self.rule_penalty(
                    similarity,
                ),

            "adjustment":
                self.rule_adjustment(
                    similarity,
                ),

            "critical_match_count":
                self.critical_match_count(
                    similarity,
                ),

            "critical_match_ratio":
                self.critical_match_ratio(
                    similarity,
                ),
        }
        
        # -----------------------------------------------------
    # Calculate Confidence
    # -----------------------------------------------------

    def calculate(
        self,
        similarity: SimilarityResult,
    ) -> float:
        """
        Calculate final confidence score.
        """

        score = (
            similarity.overall_score
            +
            self.rule_adjustment(similarity)
        )

        if self.config.normalize_score:
            score = self.normalize(score)

        return score

    # -----------------------------------------------------
    # Confidence Breakdown
    # -----------------------------------------------------

    def confidence_breakdown(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, Any]:
        """
        Detailed confidence calculation.
        """

        base_score = similarity.overall_score

        adjustment = self.rule_adjustment(
            similarity,
        )

        final_score = self.calculate(
            similarity,
        )

        return {
            "base_similarity": round(
                base_score,
                4,
            ),
            "rule_adjustment": round(
                adjustment,
                4,
            ),
            "final_confidence": round(
                final_score,
                4,
            ),
            "normalized": self.config.normalize_score,
        }

    # -----------------------------------------------------
    # Overall Confidence
    # -----------------------------------------------------

    def overall_confidence(
        self,
        similarity: SimilarityResult,
    ) -> float:
        """
        Convenience wrapper.
        """

        return self.calculate(
            similarity,
        )

    # -----------------------------------------------------
    # Confidence Delta
    # -----------------------------------------------------

    def confidence_delta(
        self,
        similarity: SimilarityResult,
    ) -> float:
        """
        Difference between similarity and confidence.
        """

        return round(
            self.calculate(similarity)
            -
            similarity.overall_score,
            4,
        )

    # -----------------------------------------------------
    # Confidence Gain
    # -----------------------------------------------------

    def confidence_gain(
        self,
        similarity: SimilarityResult,
    ) -> float:
        """
        Positive rule contribution.
        """

        gain = sum(
            self.rule_bonus(
                similarity,
            ).values()
        )

        return round(
            gain,
            4,
        )

    # -----------------------------------------------------
    # Confidence Loss
    # -----------------------------------------------------

    def confidence_loss(
        self,
        similarity: SimilarityResult,
    ) -> float:
        """
        Negative rule contribution.
        """

        loss = sum(
            self.rule_penalty(
                similarity,
            ).values()
        )

        return round(
            loss,
            4,
        )

    # -----------------------------------------------------
    # High Confidence
    # -----------------------------------------------------

    def is_high_confidence(
        self,
        similarity: SimilarityResult,
    ) -> bool:
        """
        High confidence indicator.
        """

        return (
            self.calculate(similarity)
            >=
            0.90
        )

    # -----------------------------------------------------
    # Medium Confidence
    # -----------------------------------------------------

    def is_medium_confidence(
        self,
        similarity: SimilarityResult,
    ) -> bool:
        """
        Medium confidence indicator.
        """

        score = self.calculate(
            similarity,
        )

        return (
            0.75
            <=
            score
            <
            0.90
        )

    # -----------------------------------------------------
    # Low Confidence
    # -----------------------------------------------------

    def is_low_confidence(
        self,
        similarity: SimilarityResult,
    ) -> bool:
        """
        Low confidence indicator.
        """

        return (
            self.calculate(similarity)
            <
            0.75
        )

    # -----------------------------------------------------
    # Confidence Metadata
    # -----------------------------------------------------

    def confidence_metadata(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, Any]:
        """
        Metadata describing confidence evaluation.
        """

        return {

            "confidence_level":
                self.confidence_level(
                    self.calculate(
                        similarity,
                    )
                ),

            "base_similarity":
                round(
                    similarity.overall_score,
                    4,
                ),

            "confidence_delta":
                self.confidence_delta(
                    similarity,
                ),

            "rule_bonus":
                self.rule_bonus(
                    similarity,
                ),

            "rule_penalty":
                self.rule_penalty(
                    similarity,
                ),

            "critical_match_ratio":
                self.critical_match_ratio(
                    similarity,
                ),

            "high_confidence":
                self.is_high_confidence(
                    similarity,
                ),

            "medium_confidence":
                self.is_medium_confidence(
                    similarity,
                ),

            "low_confidence":
                self.is_low_confidence(
                    similarity,
                ),
        }
        # -----------------------------------------------------
    # Decision
    # -----------------------------------------------------

    def decision(
        self,
        similarity: SimilarityResult,
    ) -> ConfidenceDecision:
        """
        Determine the final confidence decision.
        """

        score = self.calculate(
            similarity,
        )

        if self.is_auto_match(score):
            return ConfidenceDecision.AUTO_MATCH

        if self.is_manual_review(score):
            return ConfidenceDecision.MANUAL_REVIEW

        return ConfidenceDecision.NO_MATCH

    # -----------------------------------------------------
    # Requires Review
    # -----------------------------------------------------

    def requires_review(
        self,
        similarity: SimilarityResult,
    ) -> bool:
        """
        Whether manual review is required.
        """

        return (
            self.decision(similarity)
            ==
            ConfidenceDecision.MANUAL_REVIEW
        )

    # -----------------------------------------------------
    # Auto Match
    # -----------------------------------------------------

    def auto_match(
        self,
        similarity: SimilarityResult,
    ) -> bool:
        """
        Whether records qualify for auto merge.
        """

        return (
            self.decision(similarity)
            ==
            ConfidenceDecision.AUTO_MATCH
        )

    # -----------------------------------------------------
    # Reject
    # -----------------------------------------------------

    def reject(
        self,
        similarity: SimilarityResult,
    ) -> bool:
        """
        Whether records should be rejected.
        """

        return (
            self.decision(similarity)
            ==
            ConfidenceDecision.NO_MATCH
        )

    # -----------------------------------------------------
    # Review Priority
    # -----------------------------------------------------

    def priority(
        self,
        similarity: SimilarityResult,
    ) -> ReviewPriority:
        """
        Determine analyst review priority.
        """

        if self.auto_match(
            similarity,
        ):
            return ReviewPriority.NONE

        score = self.calculate(
            similarity,
        )

        ratio = self.critical_match_ratio(
            similarity,
        )

        if (
            score >= 0.90
            and
            ratio >= 0.90
        ):
            return ReviewPriority.LOW

        if (
            score >= 0.80
            and
            ratio >= 0.75
        ):
            return ReviewPriority.MEDIUM

        if score >= 0.65:
            return ReviewPriority.HIGH

        return ReviewPriority.CRITICAL

    # -----------------------------------------------------
    # Reason Codes
    # -----------------------------------------------------

    def reason_codes(
        self,
        similarity: SimilarityResult,
    ) -> List[str]:
        """
        Machine-readable decision reasons.
        """

        reasons: List[str] = []

        if similarity.name_score >= 0.90:
            reasons.append("NAME_MATCH")

        if similarity.dob_score == 1.0:
            reasons.append("DOB_MATCH")

        if similarity.phone_score == 1.0:
            reasons.append("PHONE_MATCH")

        if similarity.email_score == 1.0:
            reasons.append("EMAIL_MATCH")

        if similarity.company_score >= 0.90:
            reasons.append("COMPANY_MATCH")

        if similarity.country_score == 1.0:
            reasons.append("COUNTRY_MATCH")

        if similarity.address_score >= 0.90:
            reasons.append("ADDRESS_MATCH")

        if similarity.risk_level_score < 1.0:
            reasons.append("RISK_LEVEL_DIFFERENT")

        if (
            0.0
            <
            similarity.dob_score
            <
            1.0
        ):
            reasons.append("DOB_PARTIAL_MATCH")

        elif similarity.dob_score == 0.0:
            reasons.append("DOB_MISMATCH")

        return reasons

    # -----------------------------------------------------
    # Decision Summary
    # -----------------------------------------------------

    def decision_summary(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, Any]:
        """
        High-level decision summary.
        """

        confidence = self.calculate(
            similarity,
        )

        return {

            "decision":
                self.decision(
                    similarity,
                ).value,

            "confidence_score":
                confidence,

            "confidence_level":
                self.confidence_level(
                    confidence,
                ),

            "priority":
                self.priority(
                    similarity,
                ).value,

            "requires_review":
                self.requires_review(
                    similarity,
                ),

            "reason_codes":
                self.reason_codes(
                    similarity,
                ),
        }

    # -----------------------------------------------------
    # Evaluate
    # -----------------------------------------------------

    def evaluate(
        self,
        similarity: SimilarityResult,
    ) -> ConfidenceResult:
        """
        Convert SimilarityResult into
        ConfidenceResult.
        """

        confidence = self.calculate(
            similarity,
        )

        result = ConfidenceResult(

            left_index=similarity.left_index,

            right_index=similarity.right_index,

            similarity_score=round(
                similarity.overall_score,
                4,
            ),

            confidence_score=round(
                confidence,
                4,
            ),

            decision=self.decision(
                similarity,
            ),

            priority=self.priority(
                similarity,
            ),

            requires_review=self.requires_review(
                similarity,
            ),

            explanation=self.reason_codes(
                similarity,
            ),

            rule_scores=self.rule_score(
                similarity,
            ),

            metadata=self.confidence_metadata(
                similarity,
            ),
        )

        self.update_statistics(
            result,
        )

        return result
    
        # -----------------------------------------------------
    # Explain
    # -----------------------------------------------------

    def explain(
        self,
        similarity: SimilarityResult,
    ) -> List[str]:
        """
        Human-readable explanation of the decision.
        """

        messages: List[str] = []

        if similarity.name_score >= 0.90:
            messages.append(
                "Customer names are highly similar."
            )

        if similarity.dob_score == 1.0:
            messages.append(
                "Date of birth matches exactly."
            )

        elif similarity.dob_score > 0:
            messages.append(
                "Date of birth partially matches."
            )

        else:
            messages.append(
                "Date of birth does not match."
            )

        if similarity.phone_score == 1.0:
            messages.append(
                "Phone numbers match."
            )

        if similarity.email_score == 1.0:
            messages.append(
                "Email addresses match."
            )

        if similarity.company_score >= 0.90:
            messages.append(
                "Company information is highly similar."
            )

        if similarity.country_score == 1.0:
            messages.append(
                "Country matches."
            )

        if similarity.address_score >= 0.90:
            messages.append(
                "Addresses are highly similar."
            )

        if similarity.risk_level_score < 1.0:
            messages.append(
                "Risk profile differs."
            )

        return messages

    # -----------------------------------------------------
    # Human Summary
    # -----------------------------------------------------

    def human_summary(
        self,
        similarity: SimilarityResult,
    ) -> str:
        """
        One-line analyst summary.
        """

        decision = self.decision(
            similarity,
        ).value

        score = self.calculate(
            similarity,
        )

        return (
            f"{decision} "
            f"(confidence={score:.4f})"
        )

    # -----------------------------------------------------
    # Audit Summary
    # -----------------------------------------------------

    def audit_summary(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, Any]:
        """
        AML audit record.
        """

        return {

            "left_record":
                similarity.left_index,

            "right_record":
                similarity.right_index,

            "decision":
                self.decision(
                    similarity,
                ).value,

            "confidence":
                self.calculate(
                    similarity,
                ),

            "priority":
                self.priority(
                    similarity,
                ).value,

            "critical_match_ratio":
                self.critical_match_ratio(
                    similarity,
                ),

            "rule_scores":
                self.rule_score(
                    similarity,
                ),

            "reason_codes":
                self.reason_codes(
                    similarity,
                ),
        }

    # -----------------------------------------------------
    # Review Notes
    # -----------------------------------------------------

    def review_notes(
        self,
        similarity: SimilarityResult,
    ) -> List[str]:
        """
        Analyst review guidance.
        """

        notes: List[str] = []

        if self.requires_review(
            similarity,
        ):

            notes.append(
                "Manual review is required."
            )

            if similarity.dob_score < 1.0:
                notes.append(
                    "Verify customer's date of birth."
                )

            if similarity.phone_score < 1.0:
                notes.append(
                    "Verify phone number."
                )

            if similarity.email_score < 1.0:
                notes.append(
                    "Verify email address."
                )

            if similarity.address_score < 0.90:
                notes.append(
                    "Verify residential address."
                )

        return notes

    # -----------------------------------------------------
    # Decision Path
    # -----------------------------------------------------

    def decision_path(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, Any]:
        """
        Explain how the final decision
        was reached.
        """

        return {

            "overall_similarity":
                similarity.overall_score,

            "rule_adjustment":
                self.rule_adjustment(
                    similarity,
                ),

            "confidence":
                self.calculate(
                    similarity,
                ),

            "decision":
                self.decision(
                    similarity,
                ).value,

            "priority":
                self.priority(
                    similarity,
                ).value,
        }

    # -----------------------------------------------------
    # Investigation Summary
    # -----------------------------------------------------

    def investigation_summary(
        self,
        similarity: SimilarityResult,
    ) -> Dict[str, Any]:
        """
        Complete AML investigation summary.
        """

        return {

            "decision":
                self.decision_summary(
                    similarity,
                ),

            "confidence":
                self.confidence_breakdown(
                    similarity,
                ),

            "audit":
                self.audit_summary(
                    similarity,
                ),

            "review_notes":
                self.review_notes(
                    similarity,
                ),

            "explanation":
                self.explain(
                    similarity,
                ),
        }

    # -----------------------------------------------------
    # Printable Report
    # -----------------------------------------------------

    def printable_report(
        self,
        similarity: SimilarityResult,
    ) -> str:
        """
        Multi-line printable report.
        """

        report = []

        report.append(
            "===== Confidence Report ====="
        )

        report.append(
            f"Decision : "
            f"{self.decision(similarity).value}"
        )

        report.append(
            f"Confidence : "
            f"{self.calculate(similarity):.4f}"
        )

        report.append(
            f"Priority : "
            f"{self.priority(similarity).value}"
        )

        report.append("")

        report.append("Reasons:")

        for reason in self.explain(
            similarity,
        ):
            report.append(
                f"- {reason}"
            )

        return "\n".join(report)
    
        # -----------------------------------------------------
    # Evaluate Batch
    # -----------------------------------------------------

    def evaluate_batch(
        self,
        similarities: Iterable[SimilarityResult],
    ) -> List[ConfidenceResult]:
        """
        Evaluate an iterable of SimilarityResult objects.
        """

        results: List[ConfidenceResult] = []

        for similarity in similarities:
            results.append(
                self.evaluate(
                    similarity,
                )
            )

        return results

    # -----------------------------------------------------
    # Stream
    # -----------------------------------------------------

    def stream(
        self,
        similarities: Iterable[SimilarityResult],
    ) -> Generator[ConfidenceResult, None, None]:
        """
        Yield confidence results one at a time.
        """

        for similarity in similarities:
            yield self.evaluate(
                similarity,
            )

    # -----------------------------------------------------
    # Batch Iterator
    # -----------------------------------------------------

    def batch_iterator(
        self,
        similarities: Iterable[SimilarityResult],
        batch_size: int = 100,
    ) -> Generator[List[ConfidenceResult], None, None]:
        """
        Yield evaluated batches.
        """

        batch: List[ConfidenceResult] = []

        for similarity in similarities:

            batch.append(
                self.evaluate(
                    similarity,
                )
            )

            if len(batch) >= batch_size:
                yield batch
                batch = []

        if batch:
            yield batch

    # -----------------------------------------------------
    # Filter By Decision
    # -----------------------------------------------------

    def filter_by_decision(
        self,
        results: Iterable[ConfidenceResult],
        decision: ConfidenceDecision,
    ) -> List[ConfidenceResult]:
        """
        Filter results by decision.
        """

        return [

            result

            for result in results

            if result.decision == decision

        ]

    # -----------------------------------------------------
    # Filter By Priority
    # -----------------------------------------------------

    def filter_by_priority(
        self,
        results: Iterable[ConfidenceResult],
        priority: ReviewPriority,
    ) -> List[ConfidenceResult]:
        """
        Filter results by review priority.
        """

        return [

            result

            for result in results

            if result.priority == priority

        ]

    # -----------------------------------------------------
    # Decision Distribution
    # -----------------------------------------------------

    def distribution(
        self,
        results: Iterable[ConfidenceResult],
    ) -> Dict[str, int]:
        """
        Distribution of decisions.
        """

        distribution = {

            ConfidenceDecision.AUTO_MATCH.value: 0,

            ConfidenceDecision.MANUAL_REVIEW.value: 0,

            ConfidenceDecision.NO_MATCH.value: 0,

        }

        for result in results:

            distribution[
                result.decision.value
            ] += 1

        return distribution

    # -----------------------------------------------------
    # Priority Distribution
    # -----------------------------------------------------

    def priority_distribution(
        self,
        results: Iterable[ConfidenceResult],
    ) -> Dict[str, int]:
        """
        Distribution of review priorities.
        """

        distribution = {

            ReviewPriority.CRITICAL.value: 0,

            ReviewPriority.HIGH.value: 0,

            ReviewPriority.MEDIUM.value: 0,

            ReviewPriority.LOW.value: 0,

            ReviewPriority.NONE.value: 0,

        }

        for result in results:

            distribution[
                result.priority.value
            ] += 1

        return distribution

    # -----------------------------------------------------
    # Average Confidence
    # -----------------------------------------------------

    def average_confidence(
        self,
        results: Iterable[ConfidenceResult],
    ) -> float:
        """
        Calculate average confidence.
        """

        results = list(results)

        if not results:
            return 0.0

        return round(

            sum(
                result.confidence_score
                for result in results
            )

            /

            len(results),

            4,

        )

    # -----------------------------------------------------
    # Highest Confidence
    # -----------------------------------------------------

    def highest_confidence(
        self,
        results: Iterable[ConfidenceResult],
    ) -> Optional[ConfidenceResult]:
        """
        Return highest confidence result.
        """

        results = list(results)

        if not results:
            return None

        return max(

            results,

            key=lambda result:
                result.confidence_score,

        )

    # -----------------------------------------------------
    # Lowest Confidence
    # -----------------------------------------------------

    def lowest_confidence(
        self,
        results: Iterable[ConfidenceResult],
    ) -> Optional[ConfidenceResult]:
        """
        Return lowest confidence result.
        """

        results = list(results)

        if not results:
            return None

        return min(

            results,

            key=lambda result:
                result.confidence_score,

        )

    # -----------------------------------------------------
    # Batch Summary
    # -----------------------------------------------------

    def batch_summary(
        self,
        results: Iterable[ConfidenceResult],
    ) -> Dict[str, Any]:
        """
        Batch statistics summary.
        """

        results = list(results)

        return {

            "total_records":
                len(results),

            "average_confidence":
                self.average_confidence(
                    results,
                ),

            "decision_distribution":
                self.distribution(
                    results,
                ),

            "priority_distribution":
                self.priority_distribution(
                    results,
                ),

            "highest_confidence":
                (
                    self.highest_confidence(
                        results,
                    ).confidence_score

                    if self.highest_confidence(
                        results,
                    )

                    else None
                ),

            "lowest_confidence":
                (
                    self.lowest_confidence(
                        results,
                    ).confidence_score

                    if self.lowest_confidence(
                        results,
                    )

                    else None
                ),
        }
        # -----------------------------------------------------
    # Statistics Report
    # -----------------------------------------------------

    def statistics_report(
        self,
    ) -> Dict[str, Any]:
        """
        Return runtime statistics.
        """

        stats = self.statistics

        return {
            "processed": stats.processed,
            "auto_matches": stats.auto_matches,
            "manual_reviews": stats.manual_reviews,
            "rejected": stats.rejected,
            "cumulative_score": round(
                stats.cumulative_score,
                4,
            ),
            "average_confidence": round(
                stats.average_confidence,
                4,
            ),
        }

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    def metrics(
        self,
    ) -> Dict[str, Any]:
        """
        Production metrics.
        """

        stats = self.statistics

        processed = stats.processed

        if processed == 0:
            auto_rate = 0.0
            review_rate = 0.0
            reject_rate = 0.0
        else:
            auto_rate = round(
                stats.auto_matches / processed,
                4,
            )

            review_rate = round(
                stats.manual_reviews / processed,
                4,
            )

            reject_rate = round(
                stats.rejected / processed,
                4,
            )

        return {
            "processed_records": processed,
            "auto_match_rate": auto_rate,
            "manual_review_rate": review_rate,
            "reject_rate": reject_rate,
            "average_confidence": round(
                stats.average_confidence,
                4,
            ),
        }

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Runtime health information.
        """

        cfg = self.config
        stats = self.statistics

        return {
            "status": "healthy",
            "engine": self.__class__.__name__,
            "processed_records": stats.processed,
            "configuration_valid": (
                cfg.auto_match_threshold >
                cfg.manual_review_threshold >
                cfg.reject_threshold
            ),
            "thresholds": {
                "auto_match": cfg.auto_match_threshold,
                "manual_review": cfg.manual_review_threshold,
                "reject": cfg.reject_threshold,
            },
        }

    # -----------------------------------------------------
    # Configuration
    # -----------------------------------------------------

    def configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Return active configuration.
        """

        cfg = self.config

        return {
            "auto_match_threshold":
                cfg.auto_match_threshold,

            "manual_review_threshold":
                cfg.manual_review_threshold,

            "reject_threshold":
                cfg.reject_threshold,

            "critical_field_bonus":
                cfg.critical_field_bonus,

            "critical_field_penalty":
                cfg.critical_field_penalty,

            "phone_bonus":
                cfg.phone_bonus,

            "email_bonus":
                cfg.email_bonus,

            "dob_bonus":
                cfg.dob_bonus,

            "company_bonus":
                cfg.company_bonus,

            "country_penalty":
                cfg.country_penalty,

            "risk_penalty":
                cfg.risk_penalty,

            "normalize_score":
                cfg.normalize_score,
        }

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Overall engine summary.
        """

        return {
            "health": self.health_check(),
            "metrics": self.metrics(),
            "statistics": self.statistics_report(),
            "configuration": self.configuration(),
        }

    # -----------------------------------------------------
    # Reset Statistics
    # -----------------------------------------------------

    def reset_statistics(
        self,
    ) -> None:
        """
        Reset runtime statistics.
        """

        self.statistics = ConfidenceStatistics()

    # -----------------------------------------------------
    # Clear
    # -----------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Alias for reset_statistics().
        """

        self.reset_statistics()

    # -----------------------------------------------------
    # Print Summary
    # -----------------------------------------------------

    def print_summary(
        self,
    ) -> None:
        """
        Print engine summary.
        """

        summary = self.summary()

        print("=" * 60)
        print("Confidence Engine Summary")
        print("=" * 60)

        print()

        print("Health")
        print("------")

        for key, value in summary["health"].items():
            print(f"{key}: {value}")

        print()

        print("Metrics")
        print("-------")

        for key, value in summary["metrics"].items():
            print(f"{key}: {value}")

        print()

        print("Statistics")
        print("----------")

        for key, value in summary["statistics"].items():
            print(f"{key}: {value}")
            
        # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    def export(
        self,
        result: ConfidenceResult,
    ) -> Dict[str, Any]:
        """
        Export a ConfidenceResult as a dictionary.
        """

        return {
            "left_index": result.left_index,
            "right_index": result.right_index,
            "similarity_score": result.similarity_score,
            "confidence_score": result.confidence_score,
            "decision": result.decision.value,
            "priority": result.priority.value,
            "requires_review": result.requires_review,
            "explanation": result.explanation,
            "rule_scores": result.rule_scores,
            "metadata": result.metadata,
        }

    # -----------------------------------------------------
    # Export Batch
    # -----------------------------------------------------

    def export_batch(
        self,
        results: Iterable[ConfidenceResult],
    ) -> List[Dict[str, Any]]:
        """
        Export multiple confidence results.
        """

        return [
            self.export(result)
            for result in results
        ]

    # -----------------------------------------------------
    # To Dictionary
    # -----------------------------------------------------

    def to_dict(
        self,
        result: ConfidenceResult,
    ) -> Dict[str, Any]:
        """
        Alias for export().
        """

        return self.export(result)

    # -----------------------------------------------------
    # Has Processed
    # -----------------------------------------------------

    def has_processed(
        self,
    ) -> bool:
        """
        Whether any records have been processed.
        """

        return self.statistics.processed > 0

    # -----------------------------------------------------
    # Processed Count
    # -----------------------------------------------------

    def processed_count(
        self,
    ) -> int:
        """
        Number of processed records.
        """

        return self.statistics.processed

    # -----------------------------------------------------
    # Decision Counts
    # -----------------------------------------------------

    def decision_counts(
        self,
    ) -> Dict[str, int]:
        """
        Runtime decision counts.
        """

        stats = self.statistics

        return {
            ConfidenceDecision.AUTO_MATCH.value:
                stats.auto_matches,

            ConfidenceDecision.MANUAL_REVIEW.value:
                stats.manual_reviews,

            ConfidenceDecision.NO_MATCH.value:
                stats.rejected,
        }

    # -----------------------------------------------------
    # Runtime Snapshot
    # -----------------------------------------------------

    def runtime_snapshot(
        self,
    ) -> Dict[str, Any]:
        """
        Runtime engine snapshot.
        """

        return {

            "processed":
                self.statistics.processed,

            "average_confidence":
                self.statistics.average_confidence,

            "decision_counts":
                self.decision_counts(),

            "configuration":
                self.configuration(),

            "health":
                self.health_check(),
        }

    # -----------------------------------------------------
    # Copy Result
    # -----------------------------------------------------

    def copy_result(
        self,
        result: ConfidenceResult,
    ) -> ConfidenceResult:
        """
        Return a shallow copy of a confidence result.
        """

        return ConfidenceResult(

            left_index=result.left_index,

            right_index=result.right_index,

            similarity_score=result.similarity_score,

            confidence_score=result.confidence_score,

            decision=result.decision,

            priority=result.priority,

            requires_review=result.requires_review,

            explanation=list(result.explanation),

            rule_scores=dict(result.rule_scores),

            metadata=dict(result.metadata),
        )

    # -----------------------------------------------------
    # Merge Metadata
    # -----------------------------------------------------

    def merge_metadata(
        self,
        result: ConfidenceResult,
        metadata: Dict[str, Any],
    ) -> ConfidenceResult:
        """
        Merge additional metadata into a result.
        """

        result.metadata.update(metadata)

        return result

    # -----------------------------------------------------
    # Version
    # -----------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Engine version.
        """

        return "1.0.0"

    # -----------------------------------------------------
    # Length
    # -----------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Processed record count.
        """

        return self.statistics.processed

    # -----------------------------------------------------
    # Boolean
    # -----------------------------------------------------

    def __bool__(
        self,
    ) -> bool:
        """
        Truthy if records have been processed.
        """

        return self.statistics.processed > 0

    # -----------------------------------------------------
    # Representation
    # -----------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (

            f"{self.__class__.__name__}("

            f"processed={self.statistics.processed}, "

            f"average_confidence={self.statistics.average_confidence:.4f})"

        )

    # -----------------------------------------------------
    # String
    # -----------------------------------------------------

    def __str__(
        self,
    ) -> str:
        """
        User-friendly representation.
        """

        return (

            f"ConfidenceEngine"

            f"[processed={self.statistics.processed}, "

            f"auto={self.statistics.auto_matches}, "

            f"review={self.statistics.manual_reviews}, "

            f"reject={self.statistics.rejected}]"

        )