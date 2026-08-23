"""
==========================================================

AML Investigation Platform

Enterprise Similarity Engine

Responsibilities
----------------
✓ Compute attribute similarity
✓ Generate feature vectors
✓ Produce explainable similarity scores
✓ Support weighted scoring
✓ Generate input for Confidence Engine

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from rapidfuzz import fuzz

from app.utils.phonetic_utils import PhoneticUtils
from app.utils.blocking_utils import BlockingUtils
from app.entity_resolution.models.pipeline_results import (
    SimilarityResultSet
)

@dataclass(slots=True)
class SimilarityResult:
    """
    Stores similarity scores for a candidate pair.
    """

    left_index: int

    right_index: int

    overall_score: float = 0.0

    name_score: float = 0.0

    phonetic_score: float = 0.0

    email_score: float = 0.0

    phone_score: float = 0.0

    address_score: float = 0.0

    company_score: float = 0.0

    city_score: float = 0.0

    country_score: float = 0.0

    nationality_score: float = 0.0

    postal_score: float = 0.0

    dob_score: float = 0.0

    gender_score: float = 0.0

    customer_type_score: float = 0.0

    risk_level_score: float = 0.0

    feature_vector: Dict[str, float] = field(
        default_factory=dict
    )
    
# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


@dataclass(slots=True)
class SimilarityConfiguration:
    """
    Attribute weights used for weighted scoring.
    """

    name_weight: float = 0.25

    phonetic_weight: float = 0.05

    email_weight: float = 0.10

    phone_weight: float = 0.10

    address_weight: float = 0.10

    company_weight: float = 0.10

    city_weight: float = 0.05

    country_weight: float = 0.05

    nationality_weight: float = 0.05

    postal_weight: float = 0.02

    dob_weight: float = 0.15

    gender_weight: float = 0.02

    customer_type_weight: float = 0.03

    risk_level_weight: float = 0.03

    normalize_scores: bool = True


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


@dataclass(slots=True)
class SimilarityStatistics:

    processed_pairs: int = 0

    high_similarity: int = 0

    medium_similarity: int = 0

    low_similarity: int = 0

    average_score: float = 0.0

    total_score: float = 0.0


# ---------------------------------------------------------
# Similarity Engine
# ---------------------------------------------------------


class SimilarityEngine:
    """
    Enterprise similarity engine.
    """

    def __init__(
        self,
        config: Optional[
            SimilarityConfiguration
        ] = None,
    ):

        self.config = (
            config
            or SimilarityConfiguration()
        )

        self.statistics = SimilarityStatistics()

    # -----------------------------------------------------
    # Reset
    # -----------------------------------------------------

    def reset(self) -> None:

        self.statistics = SimilarityStatistics()

    # -----------------------------------------------------
    # Normalize Text
    # -----------------------------------------------------

    @staticmethod
    def normalize(
        value: Optional[str],
    ) -> str:
        """
        Normalize textual values before
        similarity comparison.
        """

        if value is None:
            return ""

        return str(value).strip().lower()

    # -----------------------------------------------------
    # Safe Fuzzy Score
    # -----------------------------------------------------

    @staticmethod
    def fuzzy_score(
        left: Optional[str],
        right: Optional[str],
    ) -> float:
        """
        Safe wrapper around RapidFuzz.
        Returns values between 0 and 1.
        """

        left = SimilarityEngine.normalize(left)
        right = SimilarityEngine.normalize(right)

        if not left or not right:
            return 0.0

        return (
            fuzz.token_sort_ratio(
                left,
                right,
            )
            / 100.0
        )

    # -----------------------------------------------------
    # Exact Match
    # -----------------------------------------------------

    @staticmethod
    def exact_match(
        left,
        right,
    ) -> float:
        """
        Exact comparison.
        """

        if left is None or right is None:
            return 0.0

        return (
            1.0
            if str(left).strip().lower()
            == str(right).strip().lower()
            else 0.0
        )

    # -----------------------------------------------------
    # Numeric Difference
    # -----------------------------------------------------

    @staticmethod
    def numeric_similarity(
        left,
        right,
        tolerance: float = 0.0,
    ) -> float:
        """
        Numeric comparison with tolerance.
        """

        if left is None or right is None:
            return 0.0

        try:

            left = float(left)

            right = float(right)

        except (TypeError, ValueError):

            return 0.0

        if abs(left - right) <= tolerance:
            return 1.0

        return 0.0

    # -----------------------------------------------------
    # Empty Check
    # -----------------------------------------------------
    @staticmethod
    def is_empty(
        value,
    ) -> bool:

        return value is None or str(value).strip() == ""
    
    
    # -----------------------------------------------------
    # Safe Fuzzy Score
    # -----------------------------------------------------

    @staticmethod
    def fuzzy_score(
        left: Optional[str],
        right: Optional[str],
    ) -> float:
        """
        Safe wrapper around RapidFuzz.
        Returns values between 0 and 1.
        """

        left = SimilarityEngine.normalize(left)
        right = SimilarityEngine.normalize(right)

        if not left or not right:
            return 0.0

        return (
            fuzz.token_sort_ratio(
                left,
                right,
            )
            / 100.0
        )

    # -----------------------------------------------------
    # Name Similarity
    # -----------------------------------------------------

    def name_similarity(
        self,
        left_name: Optional[str],
        right_name: Optional[str],
    ) -> float:
        """
        Compare customer names using fuzzy and phonetic matching.
        """

        fuzzy = self.fuzzy_score(
            left_name,
            right_name,
        )

        phonetic = self.phonetic_similarity(
            left_name,
            right_name,
        )

        return round(
            (fuzzy * 0.80) + (phonetic * 0.20),
            4,
        )
    # -----------------------------------------------------
    # Name Feature Vector
    # -----------------------------------------------------

    def name_features(
        self,
        left_name: Optional[str],
        right_name: Optional[str],
    ) -> Dict[str, float]:
        """
        Generate name-related feature vector.
        """

        return {

            "name_score": self.name_similarity(
                left_name,
                right_name,
            ),

            "phonetic_score": self.phonetic_similarity(
                left_name,
                right_name,
            ),
        }
        
    # -----------------------------------------------------
    # Phonetic Similarity
    # -----------------------------------------------------

    def phonetic_similarity(
        self,
        left_name: Optional[str],
        right_name: Optional[str],
    ) -> float:
        """
        Compare phonetic representation of names.
        """

        left = PhoneticUtils.soundex(left_name)
        right = PhoneticUtils.soundex(right_name)

        return self.exact_match(
            left,
            right,
        )
    # -----------------------------------------------------
    # Email Similarity
    # -----------------------------------------------------

    def email_similarity(
        self,
        left_email: Optional[str],
        right_email: Optional[str],
    ) -> float:

        return self.exact_match(
            BlockingUtils.normalize_email(left_email),
            BlockingUtils.normalize_email(right_email),
        )

    # -----------------------------------------------------
    # Email Domain Similarity
    # -----------------------------------------------------

    def email_domain_similarity(
        self,
        left_email: Optional[str],
        right_email: Optional[str],
    ) -> float:

        left = BlockingUtils.email_domain(left_email)

        right = BlockingUtils.email_domain(right_email)

        return self.exact_match(
            left,
            right,
        )

    # -----------------------------------------------------
    # Phone Similarity
    # -----------------------------------------------------

    def phone_similarity(
        self,
        left_phone: Optional[str],
        right_phone: Optional[str],
    ) -> float:

        left = BlockingUtils.normalize_phone(left_phone)

        right = BlockingUtils.normalize_phone(right_phone)

        return self.exact_match(
            left,
            right,
        )

    # -----------------------------------------------------
    # Phone Prefix Similarity
    # -----------------------------------------------------

    def phone_prefix_similarity(
        self,
        left_phone: Optional[str],
        right_phone: Optional[str],
    ) -> float:

        left = BlockingUtils.phone_prefix(left_phone)

        right = BlockingUtils.phone_prefix(right_phone)

        return self.exact_match(
            left,
            right,
        )

    # -----------------------------------------------------
    # Company Similarity
    # -----------------------------------------------------

    def company_similarity(
        self,
        left_company: Optional[str],
        right_company: Optional[str],
    ) -> float:

        left = BlockingUtils.normalize_company(
            left_company,
        )

        right = BlockingUtils.normalize_company(
            right_company,
        )

        return self.fuzzy_score(
            left,
            right,
        )

    # -----------------------------------------------------
    # Address Similarity
    # -----------------------------------------------------

    def address_similarity(
        self,
        left_address: Optional[str],
        right_address: Optional[str],
    ) -> float:

        return self.fuzzy_score(
            left_address,
            right_address,
        )

    # -----------------------------------------------------
    # Address Token Similarity
    # -----------------------------------------------------

    def address_token_similarity(
        self,
        left_address: Optional[str],
        right_address: Optional[str],
    ) -> float:

        left = self.normalize(left_address)

        right = self.normalize(right_address)

        if not left or not right:
            return 0.0

        left_tokens = set(left.split())

        right_tokens = set(right.split())

        if not left_tokens or not right_tokens:
            return 0.0

        intersection = len(
            left_tokens.intersection(right_tokens)
        )

        union = len(
            left_tokens.union(right_tokens)
        )

        return round(
            intersection / union,
            4,
        )
# -----------------------------------------------------
    # Contact Feature Vector
    # -----------------------------------------------------

    def contact_features(
        self,
        left: dict,
        right: dict,
    ) -> Dict[str, float]:
        """
        Generate contact-related features.
        """

        return {
            "email_score": self.email_similarity(
                left.get("email"),
                right.get("email"),
            ),
            "email_domain_score": self.email_domain_similarity(
                left.get("email"),
                right.get("email"),
            ),
            "phone_score": self.phone_similarity(
                left.get("phone"),
                right.get("phone"),
            ),
            "phone_prefix_score": self.phone_prefix_similarity(
                left.get("phone"),
                right.get("phone"),
            ),
            "company_score": self.company_similarity(
                left.get("company"),
                right.get("company"),
            ),
            "address_score": self.address_similarity(
                left.get("address"),
                right.get("address"),
            ),
            "address_token_score": self.address_token_similarity(
                left.get("address"),
                right.get("address"),
            ),
        }

    # -----------------------------------------------------
    # Contact Confidence
    # -----------------------------------------------------

    def contact_confidence(
        self,
        left: dict,
        right: dict,
    ) -> str:
        """
        Overall confidence for contact attributes.
        """

        features = self.contact_features(
            left,
            right,
        )

        score = (
            sum(features.values())
            /
            len(features)
        )

        if score >= 0.95:
            return "VERY_HIGH"

        if score >= 0.85:
            return "HIGH"

        if score >= 0.70:
            return "MEDIUM"

        return "LOW"
    
        # -----------------------------------------------------
    # Country Similarity
    # -----------------------------------------------------

    def country_similarity(
        self,
        left_country: Optional[str],
        right_country: Optional[str],
    ) -> float:
        """
        Compare normalized country values.
        """

        left = BlockingUtils.normalize_country(
            left_country,
        )

        right = BlockingUtils.normalize_country(
            right_country,
        )

        return self.exact_match(
            left,
            right,
        )

    # -----------------------------------------------------
    # Nationality Similarity
    # -----------------------------------------------------

    def nationality_similarity(
        self,
        left_nationality: Optional[str],
        right_nationality: Optional[str],
    ) -> float:
        """
        Compare normalized nationality values.
        """

        left = BlockingUtils.normalize_nationality(
            left_nationality,
        )

        right = BlockingUtils.normalize_nationality(
            right_nationality,
        )

        return self.exact_match(
            left,
            right,
        )

    # -----------------------------------------------------
    # City Similarity
    # -----------------------------------------------------

    def city_similarity(
        self,
        left_city: Optional[str],
        right_city: Optional[str],
    ) -> float:
        """
        Compare city names.
        """

        left = BlockingUtils.normalize_city(
            left_city,
        )

        right = BlockingUtils.normalize_city(
            right_city,
        )

        return self.fuzzy_score(
            left,
            right,
        )

    # -----------------------------------------------------
    # Postal Code Similarity
    # -----------------------------------------------------

    def postal_similarity(
        self,
        left_postal: Optional[str],
        right_postal: Optional[str],
    ) -> float:
        """
        Compare postal codes.
        """

        left = BlockingUtils.normalize_postal(
            left_postal,
        )

        right = BlockingUtils.normalize_postal(
            right_postal,
        )

        return self.exact_match(
            left,
            right,
        )

    # -----------------------------------------------------
    # Geographic Similarity
    # -----------------------------------------------------

    def geographic_similarity(
        self,
        left: dict,
        right: dict,
    ) -> float:
        """
        Overall geographic similarity.
        """

        country = self.country_similarity(
            left.get("country"),
            right.get("country"),
        )

        city = self.city_similarity(
            left.get("city"),
            right.get("city"),
        )

        nationality = self.nationality_similarity(
            left.get("nationality"),
            right.get("nationality"),
        )

        postal = self.postal_similarity(
            left.get("postal_code"),
            right.get("postal_code"),
        )

        score = (
            country * 0.35 +
            city * 0.25 +
            nationality * 0.20 +
            postal * 0.20
        )

        return round(
            score,
            4,
        )

    # -----------------------------------------------------
    # Geographic Feature Vector
    # -----------------------------------------------------

    def geographic_features(
        self,
        left: dict,
        right: dict,
    ) -> Dict[str, float]:
        """
        Geographic feature vector.
        """

        return {
            "country_score": self.country_similarity(
                left.get("country"),
                right.get("country"),
            ),
            "city_score": self.city_similarity(
                left.get("city"),
                right.get("city"),
            ),
            "nationality_score": self.nationality_similarity(
                left.get("nationality"),
                right.get("nationality"),
            ),
            "postal_score": self.postal_similarity(
                left.get("postal_code"),
                right.get("postal_code"),
            ),
            "geographic_score": self.geographic_similarity(
                left,
                right,
            ),
        }

    # -----------------------------------------------------
    # Geographic Confidence
    # -----------------------------------------------------

    def geographic_confidence(
        self,
        left: dict,
        right: dict,
    ) -> str:
        """
        Confidence of geographic match.
        """

        score = self.geographic_similarity(
            left,
            right,
        )

        if score >= 0.95:
            return "VERY_HIGH"

        if score >= 0.80:
            return "HIGH"

        if score >= 0.60:
            return "MEDIUM"

        return "LOW"

    # -----------------------------------------------------
    # Region Match
    # -----------------------------------------------------

    def same_region(
        self,
        left: dict,
        right: dict,
    ) -> bool:
        """
        Determine whether two records belong
        to the same region.
        """

        return (
            self.country_similarity(
                left.get("country"),
                right.get("country"),
            ) == 1.0
            and
            self.city_similarity(
                left.get("city"),
                right.get("city"),
            ) >= 0.90
        )

    # -----------------------------------------------------
    # Country Only Match
    # -----------------------------------------------------

    def same_country(
        self,
        left_country: Optional[str],
        right_country: Optional[str],
    ) -> bool:

        return (
            self.country_similarity(
                left_country,
                right_country,
            ) == 1.0
        )

    # -----------------------------------------------------
    # Postal Match
    # -----------------------------------------------------

    def same_postal(
        self,
        left_postal: Optional[str],
        right_postal: Optional[str],
    ) -> bool:

        return (
            self.postal_similarity(
                left_postal,
                right_postal,
            ) == 1.0
        )
        
            # -----------------------------------------------------
    # Date of Birth Similarity
    # -----------------------------------------------------

    def dob_similarity(
        self,
        left_dob,
        right_dob,
    ) -> float:
        """
        Compare date of birth.
        """

        return self.exact_match(
            left_dob,
            right_dob,
        )

    # -----------------------------------------------------
    # Gender Similarity
    # -----------------------------------------------------

    def gender_similarity(
        self,
        left_gender: Optional[str],
        right_gender: Optional[str],
    ) -> float:
        """
        Compare gender values.
        """

        return self.exact_match(
            self.normalize(left_gender),
            self.normalize(right_gender),
        )

    # -----------------------------------------------------
    # Customer Type Similarity
    # -----------------------------------------------------

    def customer_type_similarity(
        self,
        left_type: Optional[str],
        right_type: Optional[str],
    ) -> float:
        """
        Compare customer type.
        """

        left = BlockingUtils.normalize_customer_type(
            left_type,
        )

        right = BlockingUtils.normalize_customer_type(
            right_type,
        )

        return self.exact_match(
            left,
            right,
        )

    # -----------------------------------------------------
    # Risk Level Similarity
    # -----------------------------------------------------

    def risk_level_similarity(
        self,
        left_level: Optional[str],
        right_level: Optional[str],
    ) -> float:
        """
        Compare AML risk level.
        """

        left = BlockingUtils.normalize_risk_level(
            left_level,
        )

        right = BlockingUtils.normalize_risk_level(
            right_level,
        )

        return self.exact_match(
            left,
            right,
        )

    # -----------------------------------------------------
    # Identity Similarity
    # -----------------------------------------------------

    def identity_similarity(
        self,
        left: dict,
        right: dict,
    ) -> float:
        """
        Composite identity similarity.
        """

        dob = self.dob_similarity(
            left.get("dob"),
            right.get("dob"),
        )

        gender = self.gender_similarity(
            left.get("gender"),
            right.get("gender"),
        )

        customer = self.customer_type_similarity(
            left.get("customer_type"),
            right.get("customer_type"),
        )

        risk = self.risk_level_similarity(
            left.get("risk_level"),
            right.get("risk_level"),
        )

        score = (
            dob * 0.60 +
            gender * 0.10 +
            customer * 0.20 +
            risk * 0.10
        )

        return round(score, 4)

    # -----------------------------------------------------
    # Identity Feature Vector
    # -----------------------------------------------------

    def identity_features(
        self,
        left: dict,
        right: dict,
    ) -> Dict[str, float]:
        """
        Identity-related features.
        """

        return {
            "dob_score": self.dob_similarity(
                left.get("dob"),
                right.get("dob"),
            ),
            "gender_score": self.gender_similarity(
                left.get("gender"),
                right.get("gender"),
            ),
            "customer_type_score": self.customer_type_similarity(
                left.get("customer_type"),
                right.get("customer_type"),
            ),
            "risk_level_score": self.risk_level_similarity(
                left.get("risk_level"),
                right.get("risk_level"),
            ),
            "identity_score": self.identity_similarity(
                left,
                right,
            ),
        }

    # -----------------------------------------------------
    # Identity Confidence
    # -----------------------------------------------------

    def identity_confidence(
        self,
        left: dict,
        right: dict,
    ) -> str:
        """
        Confidence for identity attributes.
        """

        score = self.identity_similarity(
            left,
            right,
        )

        if score >= 0.95:
            return "VERY_HIGH"

        if score >= 0.85:
            return "HIGH"

        if score >= 0.70:
            return "MEDIUM"

        return "LOW"

    # -----------------------------------------------------
    # Same Identity
    # -----------------------------------------------------

    def same_identity(
        self,
        left: dict,
        right: dict,
    ) -> bool:
        """
        Determine whether two records share
        the same core identity.
        """

        return (
            self.dob_similarity(
                left.get("dob"),
                right.get("dob"),
            ) == 1.0
            and
            self.name_similarity(
                left.get("name"),
                right.get("name"),
            ) >= 0.90
        )

    # -----------------------------------------------------
    # Identity Match Rule
    # -----------------------------------------------------

    def identity_match(
        self,
        left: dict,
        right: dict,
        threshold: float = 0.85,
    ) -> bool:
        """
        Rule-based identity match.
        """

        return (
            self.identity_similarity(
                left,
                right,
            ) >= threshold
        )

    # -----------------------------------------------------
    # Identity Summary
    # -----------------------------------------------------

    def identity_summary(
        self,
        left: dict,
        right: dict,
    ) -> Dict[str, object]:
        """
        Human-readable identity summary.
        """

        return {
            "identity_score": self.identity_similarity(
                left,
                right,
            ),
            "confidence": self.identity_confidence(
                left,
                right,
            ),
            "same_identity": self.same_identity(
                left,
                right,
            ),
            "features": self.identity_features(
                left,
                right,
            ),
        }
        
    # -----------------------------------------------------
    # Feature Vector
    # -----------------------------------------------------

    def build_feature_vector(
        self,
        left: dict,
        right: dict,
    ) -> Dict[str, float]:
        """
        Build complete feature vector.
        """

        features = {}

        features.update(
            self.name_features(
                left.get("name"),
                right.get("name"),
            )
        )

        features.update(
            self.contact_features(
                left,
                right,
            )
        )

        features.update(
            self.geographic_features(
                left,
                right,
            )
        )

        features.update(
            self.identity_features(
                left,
                right,
            )
        )

        return features

    # -----------------------------------------------------
    # Weighted Score
    # -----------------------------------------------------

    def weighted_score(
        self,
        features: Dict[str, float],
    ) -> float:
        """
        Compute weighted similarity score.
        """

        cfg = self.config

        score = (
            features.get("name_score", 0.0)
            * cfg.name_weight +

            features.get("phonetic_score", 0.0)
            * cfg.phonetic_weight +

            features.get("email_score", 0.0)
            * cfg.email_weight +

            features.get("phone_score", 0.0)
            * cfg.phone_weight +

            features.get("address_score", 0.0)
            * cfg.address_weight +

            features.get("company_score", 0.0)
            * cfg.company_weight +

            features.get("city_score", 0.0)
            * cfg.city_weight +

            features.get("country_score", 0.0)
            * cfg.country_weight +

            features.get("nationality_score", 0.0)
            * cfg.nationality_weight +

            features.get("postal_score", 0.0)
            * cfg.postal_weight +

            features.get("dob_score", 0.0)
            * cfg.dob_weight +

            features.get("gender_score", 0.0)
            * cfg.gender_weight +

            features.get("customer_type_score", 0.0)
            * cfg.customer_type_weight +

            features.get("risk_level_score", 0.0)
            * cfg.risk_level_weight
        )

        return round(score, 4)

    # -----------------------------------------------------
    # Similarity Level
    # -----------------------------------------------------

    @staticmethod
    def similarity_level(
        score: float,
    ) -> str:

        if score >= 0.95:
            return "VERY_HIGH"

        if score >= 0.85:
            return "HIGH"

        if score >= 0.70:
            return "MEDIUM"

        if score >= 0.50:
            return "LOW"

        return "VERY_LOW"

    # -----------------------------------------------------
    # Compare Records
    # -----------------------------------------------------

    def compare(
        self,
        left_index: int,
        right_index: int,
        left: dict,
        right: dict,
    ) -> SimilarityResult:
        """
        Compare two customer records.
        """

        features = self.build_feature_vector(
            left,
            right,
        )

        overall = self.weighted_score(
            features,
        )

        result = SimilarityResult(
            left_index=left_index,
            right_index=right_index,
            overall_score=overall,

            name_score=features.get(
                "name_score",
                0.0,
            ),

            phonetic_score=features.get(
                "phonetic_score",
                0.0,
            ),

            email_score=features.get(
                "email_score",
                0.0,
            ),

            phone_score=features.get(
                "phone_score",
                0.0,
            ),

            address_score=features.get(
                "address_score",
                0.0,
            ),

            company_score=features.get(
                "company_score",
                0.0,
            ),

            city_score=features.get(
                "city_score",
                0.0,
            ),

            country_score=features.get(
                "country_score",
                0.0,
            ),

            nationality_score=features.get(
                "nationality_score",
                0.0,
            ),

            postal_score=features.get(
                "postal_score",
                0.0,
            ),

            dob_score=features.get(
                "dob_score",
                0.0,
            ),

            gender_score=features.get(
                "gender_score",
                0.0,
            ),

            customer_type_score=features.get(
                "customer_type_score",
                0.0,
            ),

            risk_level_score=features.get(
                "risk_level_score",
                0.0,
            ),

            feature_vector=features,
        )

        self.statistics.processed_pairs += 1

        self.statistics.total_score += overall

        self.statistics.average_score = round(
            self.statistics.total_score
            /
            self.statistics.processed_pairs,
            4,
        )

        level = self.similarity_level(
            overall,
        )

        if level == "VERY_HIGH":
            self.statistics.high_similarity += 1

        elif level in ("HIGH", "MEDIUM"):
            self.statistics.medium_similarity += 1

        else:
            self.statistics.low_similarity += 1

        return result

    # -----------------------------------------------------
    # Explain Match
    # -----------------------------------------------------

    def explain(
        self,
        result: SimilarityResult,
    ) -> Dict[str, object]:
        """
        Explain why two records matched.
        """

        return {
            "overall_score": result.overall_score,
            "level": self.similarity_level(
                result.overall_score,
            ),
            "feature_vector": result.feature_vector,
        }

    # -----------------------------------------------------
    # Match Decision
    # -----------------------------------------------------

    def is_match(
        self,
        result: SimilarityResult,
        threshold: float = 0.85,
    ) -> bool:
        """
        Rule-based match decision.
        """

        return (
            result.overall_score
            >= threshold
        )
        
    # -----------------------------------------------------
    # Compare Candidate List
    # -----------------------------------------------------

    def compare_candidates(
        self,
        candidates,
        records: List[dict],
    ) -> SimilarityResultSet:
        """
        Compare a list of CandidatePair objects.
        """

        results: List[SimilarityResult] = []

        for candidate in candidates:

            left = records[candidate.left_index]

            right = records[candidate.right_index]

            result = self.compare(
                left_index=candidate.left_index,
                right_index=candidate.right_index,
                left=left,
                right=right,
            )

            results.append(result)

        
        # -----------------------------------------------------
        # Pipeline Statistics
        # -----------------------------------------------------

        processed_pairs = len(results)

        matched_pairs = sum(
            1
            for r in results
            if self.is_match(r)
        )

        average_similarity = self.average_similarity(
            results
        )

        highest_similarity = (
            max(
                r.overall_score
                for r in results
            )
            if results
            else 0.0
        )

        lowest_similarity = (
            min(
                r.overall_score
                for r in results
            )
            if results
            else 0.0
        )
        return SimilarityResultSet(

            results=results,

            processed_pairs=processed_pairs,

            matched_pairs=matched_pairs,

            average_similarity=average_similarity,

            highest_similarity=highest_similarity,

            lowest_similarity=lowest_similarity,

            processing_time=0.0,

        )

    # -----------------------------------------------------
    # Batch Compare
    # -----------------------------------------------------

    def batch_compare(
        self,
        candidates,
        records: List[dict],
        batch_size: int = 500,
    ):
   

        batch: List[SimilarityResult] = []

        for candidate in candidates:

            result = self.compare(
                left_index=candidate.left_index,
                right_index=candidate.right_index,
                left=records[candidate.left_index],
                right=records[candidate.right_index],
            )

            batch.append(result)

            if len(batch) >= batch_size:

                yield batch

                batch = []

        if batch:

            yield batch

    # -----------------------------------------------------
    # Stream Compare
    # -----------------------------------------------------

    def stream_compare(
        self,
        candidates,
        records: List[dict],
    ):
        """
        Stream similarity results one at a time.
        """

        for candidate in candidates:

            yield self.compare(
                candidate.left_index,
                candidate.right_index,
                records[candidate.left_index],
                records[candidate.right_index],
            )

    # -----------------------------------------------------
    # Filter Matches
    # -----------------------------------------------------

    def filter_matches(
        self,
        results: List[SimilarityResult],
        threshold: float = 0.85,
    ) -> List[SimilarityResult]:
        """
        Keep only matched results.
        """

        return [
            result
            for result in results
            if result.overall_score >= threshold
        ]

    # -----------------------------------------------------
    # Top Matches
    # -----------------------------------------------------

    def top_matches(
        self,
        results: List[SimilarityResult],
        limit: int = 100,
    ) -> List[SimilarityResult]:
        """
        Highest similarity first.
        """

        return sorted(
            results,
            key=lambda r: r.overall_score,
            reverse=True,
        )[:limit]

    # -----------------------------------------------------
    # Average Score
    # -----------------------------------------------------

    def average_similarity(
        self,
        results: List[SimilarityResult],
    ) -> float:

        if not results:
            return 0.0

        return round(
            sum(
                r.overall_score
                for r in results
            ) / len(results),
            4,
        )

    # -----------------------------------------------------
    # Similarity Distribution
    # -----------------------------------------------------

    def similarity_distribution(
        self,
        results: List[SimilarityResult],
    ) -> Dict[str, int]:
        """
        Distribution by similarity level.
        """

        distribution = {
            "VERY_HIGH": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "VERY_LOW": 0,
        }

        for result in results:

            level = self.similarity_level(
                result.overall_score,
            )

            distribution[level] += 1

        return distribution

    # -----------------------------------------------------
    # Match Rate
    # -----------------------------------------------------

    def match_rate(
        self,
        results: List[SimilarityResult],
        threshold: float = 0.85,
    ) -> float:
        """
        Percentage of candidate pairs
        considered matches.
        """

        if not results:
            return 0.0

        matched = len(
            self.filter_matches(
                results,
                threshold,
            )
        )

        return round(
            matched / len(results),
            4,
        )

    # -----------------------------------------------------
    # Best Match
    # -----------------------------------------------------

    def best_match(
        self,
        results: List[SimilarityResult],
    ) -> Optional[SimilarityResult]:

        if not results:
            return None

        return max(
            results,
            key=lambda r: r.overall_score,
        )

    # -----------------------------------------------------
    # Worst Match
    # -----------------------------------------------------

    def worst_match(
        self,
        results: List[SimilarityResult],
    ) -> Optional[SimilarityResult]:

        if not results:
            return None

        return min(
            results,
            key=lambda r: r.overall_score,
        )
            # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    def statistics_report(self) -> Dict[str, object]:
        """
        Return processing statistics.
        """

        return {
            "processed_pairs": self.statistics.processed_pairs,
            "high_similarity": self.statistics.high_similarity,
            "medium_similarity": self.statistics.medium_similarity,
            "low_similarity": self.statistics.low_similarity,
            "average_score": round(
                self.statistics.average_score,
                4,
            ),
        }

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(self) -> Dict[str, object]:
        """
        Engine health information.
        """

        return {
            "healthy": True,
            "engine": self.__class__.__name__,
            "processed_pairs": self.statistics.processed_pairs,
            "configuration_loaded": self.config is not None,
        }

    # -----------------------------------------------------
    # Configuration
    # -----------------------------------------------------

    def configuration(self) -> Dict[str, float]:
        """
        Active similarity weights.
        """

        return {
            "name_weight": self.config.name_weight,
            "phonetic_weight": self.config.phonetic_weight,
            "email_weight": self.config.email_weight,
            "phone_weight": self.config.phone_weight,
            "address_weight": self.config.address_weight,
            "company_weight": self.config.company_weight,
            "city_weight": self.config.city_weight,
            "country_weight": self.config.country_weight,
            "nationality_weight": self.config.nationality_weight,
            "postal_weight": self.config.postal_weight,
            "dob_weight": self.config.dob_weight,
            "gender_weight": self.config.gender_weight,
            "customer_type_weight": self.config.customer_type_weight,
            "risk_level_weight": self.config.risk_level_weight,
        }

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    def summary(self) -> Dict[str, object]:
        """
        Complete engine summary.
        """

        return {
            "engine": self.__class__.__name__,
            "statistics": self.statistics_report(),
            "configuration": self.configuration(),
            "health": self.health_check(),
        }

    # -----------------------------------------------------
    # Print Summary
    # -----------------------------------------------------

    def print_summary(self) -> None:
        """
        Print engine summary.
        """

        summary = self.summary()

        print("\n========== Similarity Engine ==========")

        print(
            f"Processed Pairs : "
            f"{summary['statistics']['processed_pairs']}"
        )

        print(
            f"Average Score   : "
            f"{summary['statistics']['average_score']}"
        )

        print(
            f"High Similarity : "
            f"{summary['statistics']['high_similarity']}"
        )

        print(
            f"Medium Similarity : "
            f"{summary['statistics']['medium_similarity']}"
        )

        print(
            f"Low Similarity : "
            f"{summary['statistics']['low_similarity']}"
        )

        print(
            f"Healthy : "
            f"{summary['health']['healthy']}"
        )

        print("=======================================\n")

    # -----------------------------------------------------
    # Reset Statistics
    # -----------------------------------------------------

    def reset_statistics(self) -> None:
        """
        Reset runtime statistics.
        """

        self.statistics = SimilarityStatistics()

    # -----------------------------------------------------
    # Clear
    # -----------------------------------------------------

    def clear(self) -> None:
        """
        Reset engine state.
        """

        self.reset_statistics()

    # -----------------------------------------------------
    # Container Utilities
    # -----------------------------------------------------

    def __len__(self) -> int:
        """
        Number of processed pairs.
        """

        return self.statistics.processed_pairs

    def __bool__(self) -> bool:
        """
        Engine has processed data.
        """

        return self.statistics.processed_pairs > 0

    def __repr__(self) -> str:
        """
        String representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"processed_pairs={self.statistics.processed_pairs}, "
            f"average_score={self.statistics.average_score:.4f})"
        )
        
    