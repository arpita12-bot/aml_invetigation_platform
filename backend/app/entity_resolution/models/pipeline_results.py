"""
==========================================================
AML Investigation Platform

Pipeline Result Models

Standardized return types for the Entity Resolution pipeline.
==========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ---------------------------------------------------------
# Blocking
# ---------------------------------------------------------

@dataclass
class BlockingResult:

    block_index: dict[str, list[int]]

    total_records: int

    total_blocks: int

    largest_block: int

    average_block_size: float

    singleton_blocks: int

    generated_at: datetime = field(
        default_factory=datetime.utcnow
    )


# ---------------------------------------------------------
# Candidate Generation
# ---------------------------------------------------------

@dataclass
class CandidateResult:

    candidate_pairs: list[Any]

    total_candidates: int

    duplicate_candidates_removed: int

    generated_at: datetime = field(
        default_factory=datetime.utcnow
    )

# ---------------------------------------------------------
# Confidence
# ---------------------------------------------------------

@dataclass
class ConfidenceResultSet:

    results: list[Any]

    automatic_matches: int

    manual_review: int

    rejected: int

    generated_at: datetime = field(
        default_factory=datetime.utcnow
    )


# ---------------------------------------------------------
# Persistence
# ---------------------------------------------------------

@dataclass
class PersistenceResult:

    inserted: int

    updated: int

    review_records: int

    execution_time: float

    generated_at: datetime = field(
        default_factory=datetime.utcnow
    )


# ---------------------------------------------------------
# Neo4j
# ---------------------------------------------------------

@dataclass
class GraphSyncResult:
    
    indexes_created: int = 0

    nodes_created: int

    relationships_created: int

    execution_time: float

    generated_at: datetime = field(
        default_factory=datetime.utcnow
    )
    
# ---------------------------------------------------------
# Similarity
# ---------------------------------------------------------

@dataclass
class SimilarityResultSet:

    results: list[Any]

    processed_pairs: int

    matched_pairs: int

    average_similarity: float

    highest_similarity: float

    lowest_similarity: float

    processing_time: float

    generated_at: datetime = field(
        default_factory=datetime.utcnow
    )