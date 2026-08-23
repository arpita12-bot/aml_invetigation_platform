"""
==========================================================

AML Investigation Platform

Enterprise Candidate Generator

Responsibilities
----------------
✓ Generate unique candidate pairs
✓ Remove duplicate comparisons
✓ Track blocking strategies
✓ Support batch generation
✓ Produce candidate statistics

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Dict, Iterator, List, Optional, Set, Tuple


# ---------------------------------------------------------
# Candidate Pair
# ---------------------------------------------------------


@dataclass(slots=True)
class CandidatePair:
    """
    Represents a unique candidate pair.
    """

    left_index: int

    right_index: int

    block_keys: Set[str] = field(default_factory=set)

    match_count: int = 0

    def add_strategy(self, block_key: str) -> None:
        """
        Register a blocking strategy.
        """

        self.block_keys.add(block_key)

        self.match_count = len(self.block_keys)

    @property
    def pair(self) -> Tuple[int, int]:

        return (
            self.left_index,
            self.right_index,
        )


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


@dataclass(slots=True)
class CandidateStatistics:

    total_blocks: int = 0

    processed_blocks: int = 0

    total_pairs: int = 0

    duplicate_pairs: int = 0

    skipped_self_pairs: int = 0

    unique_pairs: int = 0


# ---------------------------------------------------------
# Candidate Generator
# ---------------------------------------------------------


class CandidateGenerator:
    """
    Enterprise Candidate Generator.
    """

    def __init__(self):

        self._pairs: Dict[
            Tuple[int, int],
            CandidatePair,
        ] = {}

        self.statistics = CandidateStatistics()

    # -----------------------------------------------------
    # Reset
    # -----------------------------------------------------

    def reset(self) -> None:

        self._pairs.clear()

        self.statistics = CandidateStatistics()

    # -----------------------------------------------------
    # Normalize Pair
    # -----------------------------------------------------

    @staticmethod
    def normalize_pair(
        left: int,
        right: int,
    ) -> Tuple[int, int]:
        """
        Ensure consistent ordering.

        (8,2)

        →

        (2,8)
        """

        if left < right:
            return left, right

        return right, left

    # -----------------------------------------------------
    # Pair Exists
    # -----------------------------------------------------

    def exists(
        self,
        left: int,
        right: int,
    ) -> bool:

        pair = self.normalize_pair(
            left,
            right,
        )

        return pair in self._pairs

    # -----------------------------------------------------
    # Get Pair
    # -----------------------------------------------------

    def get(
        self,
        left: int,
        right: int,
    ) -> Optional[CandidatePair]:

        pair = self.normalize_pair(
            left,
            right,
        )

        return self._pairs.get(pair)

    # -----------------------------------------------------
    # Add Pair
    # -----------------------------------------------------

    def add_pair(
        self,
        left: int,
        right: int,
        block_key: str,
    ) -> None:
        """
        Add or update a candidate pair.
        """

        if left == right:

            self.statistics.skipped_self_pairs += 1

            return

        pair = self.normalize_pair(
            left,
            right,
        )

        if pair not in self._pairs:

            candidate = CandidatePair(
                left_index=pair[0],
                right_index=pair[1],
            )

            candidate.add_strategy(block_key)

            self._pairs[pair] = candidate

        else:

            self.statistics.duplicate_pairs += 1

            self._pairs[pair].add_strategy(
                block_key
            )

    # -----------------------------------------------------
    # Pair Count
    # -----------------------------------------------------

    def pair_count(self) -> int:

        return len(self._pairs)

    # -----------------------------------------------------
    # All Pairs
    # -----------------------------------------------------

    def pairs(self) -> List[CandidatePair]:

        return list(self._pairs.values())

    # -----------------------------------------------------
    # Clear
    # -----------------------------------------------------

    def clear(self) -> None:

        self.reset()
        
        
        # -----------------------------------------------------
    # Process Single Block
    # -----------------------------------------------------

    def process_block(
        self,
        block_key: str,
        members: List[int],
    ) -> None:
        """
        Generate candidate pairs for a single block.
        """

        self.statistics.processed_blocks += 1

        if len(members) < 2:
            return

        for left, right in combinations(members, 2):

            self.add_pair(
                left=left,
                right=right,
                block_key=block_key,
            )

    # -----------------------------------------------------
    # Process Multiple Blocks
    # -----------------------------------------------------

    def process_blocks(
        self,
        blocks: Dict[str, List[int]],
    ) -> None:
        """
        Process all blocking results.
        """

        self.reset()

        self.statistics.total_blocks = len(blocks)

        for block_key, members in blocks.items():

            self.process_block(
                block_key=block_key,
                members=members,
            )

        self.statistics.unique_pairs = len(
            self._pairs
        )

        self.statistics.total_pairs = sum(
            max(0, len(members) * (len(members) - 1) // 2)
            for members in blocks.values()
        )

    # -----------------------------------------------------
    # Process Selected Blocks
    # -----------------------------------------------------

    def process_selected_blocks(
        self,
        blocks: Dict[str, List[int]],
        selected_keys: List[str],
    ) -> None:
        """
        Process only selected block keys.
        """

        for block_key in selected_keys:

            members = blocks.get(block_key)

            if members is None:
                continue

            self.process_block(
                block_key,
                members,
            )

    # -----------------------------------------------------
    # Generate Candidate Pairs
    # -----------------------------------------------------

    def generate(
        self,
        blocks: Dict[str, List[int]],
    ) -> List[CandidatePair]:
        """
        Main entry point.

        Returns all unique candidate pairs.
        """

        self.process_blocks(blocks)

        return self.pairs()

    # -----------------------------------------------------
    # Candidate Iterator
    # -----------------------------------------------------

    def iter_pairs(
        self,
    ) -> Iterator[CandidatePair]:
        """
        Iterate over generated candidate pairs.
        """

        yield from self._pairs.values()

    # -----------------------------------------------------
    # Candidate Keys
    # -----------------------------------------------------

    def pair_keys(
        self,
    ) -> List[Tuple[int, int]]:
        """
        Return all normalized pair keys.
        """

        return list(self._pairs.keys())

    # -----------------------------------------------------
    # Pair Strategies
    # -----------------------------------------------------

    def pair_strategies(
        self,
        left: int,
        right: int,
    ) -> Set[str]:
        """
        Return the blocking strategies that
        produced the candidate pair.
        """

        candidate = self.get(
            left,
            right,
        )

        if candidate is None:
            return set()

        return candidate.block_keys.copy()

    # -----------------------------------------------------
    # Pair Weight
    # -----------------------------------------------------

    def pair_weight(
        self,
        left: int,
        right: int,
    ) -> int:
        """
        Number of blocking strategies that
        generated the pair.
        """

        candidate = self.get(
            left,
            right,
        )

        if candidate is None:
            return 0

        return candidate.match_count
    
        # -----------------------------------------------------
    # Stream Candidates
    # -----------------------------------------------------

    def stream_candidates(
        self,
        blocks: Dict[str, List[int]],
    ) -> Iterator[CandidatePair]:
        """
        Generate candidates as a stream.

        Suitable for very large datasets.
        """

        self.reset()

        self.statistics.total_blocks = len(blocks)

        for block_key, members in blocks.items():

            self.statistics.processed_blocks += 1

            if len(members) < 2:
                continue

            for left, right in combinations(members, 2):

                self.add_pair(
                    left,
                    right,
                    block_key,
                )

        for pair in self._pairs.values():
            yield pair

        self.statistics.unique_pairs = len(
            self._pairs
        )

    # -----------------------------------------------------
    # Batch Iterator
    # -----------------------------------------------------

    def batch_iterator(
        self,
        batch_size: int = 1000,
    ) -> Iterator[List[CandidatePair]]:
        """
        Yield candidate pairs in batches.
        """

        values = list(self._pairs.values())

        for start in range(
            0,
            len(values),
            batch_size,
        ):

            yield values[
                start:start + batch_size
            ]

    # -----------------------------------------------------
    # Filter Candidates
    # -----------------------------------------------------

    def filter_candidates(
        self,
        minimum_weight: int = 1,
    ) -> List[CandidatePair]:
        """
        Keep only candidates generated by
        at least the specified number of
        blocking strategies.
        """

        return [
            pair
            for pair in self._pairs.values()
            if pair.match_count >= minimum_weight
        ]

    # -----------------------------------------------------
    # Top Candidates
    # -----------------------------------------------------

    def top_candidates(
        self,
        limit: int = 100,
    ) -> List[CandidatePair]:
        """
        Return highest weighted candidates.
        """

        return sorted(
            self._pairs.values(),
            key=lambda p: p.match_count,
            reverse=True,
        )[:limit]

    # -----------------------------------------------------
    # Candidate Distribution
    # -----------------------------------------------------

    def weight_distribution(
        self,
    ) -> Dict[int, int]:
        """
        Distribution of candidate weights.

        Example

        {
            1: 900,
            2: 410,
            3: 67
        }
        """

        distribution: Dict[int, int] = {}

        for pair in self._pairs.values():

            weight = pair.match_count

            distribution[weight] = (
                distribution.get(weight, 0) + 1
            )

        return distribution

    # -----------------------------------------------------
    # Candidate Lookup
    # -----------------------------------------------------

    def lookup(
        self,
        index: int,
    ) -> List[CandidatePair]:
        """
        Return every candidate containing
        the specified record.
        """

        return [
            pair
            for pair in self._pairs.values()
            if pair.left_index == index
            or pair.right_index == index
        ]

    # -----------------------------------------------------
    # Candidate Count
    # -----------------------------------------------------

    def candidate_count_for_record(
        self,
        index: int,
    ) -> int:
        """
        Number of candidates involving
        a given record.
        """

        return len(
            self.lookup(index)
        )

    # -----------------------------------------------------
    # Maximum Weight
    # -----------------------------------------------------

    def maximum_weight(self) -> int:
        """
        Highest blocking weight observed.
        """

        if not self._pairs:
            return 0

        return max(
            pair.match_count
            for pair in self._pairs.values()
        )

    # -----------------------------------------------------
    # Average Weight
    # -----------------------------------------------------

    def average_weight(self) -> float:
        """
        Average number of blocking
        strategies per candidate.
        """

        if not self._pairs:
            return 0.0

        return (
            sum(
                pair.match_count
                for pair in self._pairs.values()
            )
            /
            len(self._pairs)
        )
        
        # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    def statistics_report(self) -> dict:
        """
        Return candidate generation statistics.
        """

        return {
            "total_blocks": self.statistics.total_blocks,
            "processed_blocks": self.statistics.processed_blocks,
            "generated_pairs": self.statistics.total_pairs,
            "unique_pairs": self.statistics.unique_pairs,
            "duplicate_pairs": self.statistics.duplicate_pairs,
            "skipped_self_pairs": self.statistics.skipped_self_pairs,
            "average_weight": round(
                self.average_weight(),
                2,
            ),
            "maximum_weight": self.maximum_weight(),
        }

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(self) -> dict:
        """
        Perform generator health check.
        """

        return {
            "healthy": len(self._pairs) > 0,
            "pair_count": self.pair_count(),
            "processed_blocks": self.statistics.processed_blocks,
            "average_weight": round(
                self.average_weight(),
                2,
            ),
        }

    # -----------------------------------------------------
    # Reduction Ratio
    # -----------------------------------------------------

    def reduction_ratio(
        self,
    ) -> float:
        """
        Percentage of duplicate comparisons removed.
        """

        generated = self.statistics.total_pairs

        if generated == 0:
            return 1.0

        unique = self.statistics.unique_pairs

        return round(
            1 - (unique / generated),
            4,
        )

    # -----------------------------------------------------
    # Candidate Summary
    # -----------------------------------------------------

    def summary(self) -> dict:
        """
        Complete summary.
        """

        return {
            "statistics": self.statistics_report(),
            "health": self.health_check(),
            "weight_distribution": self.weight_distribution(),
        }

    # -----------------------------------------------------
    # Print Summary
    # -----------------------------------------------------

    def print_summary(
        self,
    ) -> None:
        """
        Print generator summary.
        """

        stats = self.statistics_report()

        print("=" * 60)
        print("Enterprise Candidate Generator Summary")
        print("=" * 60)

        print(f"Blocks Processed : {stats['processed_blocks']}")
        print(f"Generated Pairs : {stats['generated_pairs']}")
        print(f"Unique Pairs    : {stats['unique_pairs']}")
        print(f"Duplicate Pairs : {stats['duplicate_pairs']}")
        print(f"Average Weight  : {stats['average_weight']}")
        print(f"Maximum Weight  : {stats['maximum_weight']}")
        print(f"Reduction Ratio : {self.reduction_ratio()}")

        print("=" * 60)

    # -----------------------------------------------------
    # Empty Check
    # -----------------------------------------------------

    def is_empty(
        self,
    ) -> bool:

        return len(self._pairs) == 0

    # -----------------------------------------------------
    # Contains
    # -----------------------------------------------------

    def contains(
        self,
        left: int,
        right: int,
    ) -> bool:

        return self.exists(
            left,
            right,
        )

    # -----------------------------------------------------
    # Export Pairs
    # -----------------------------------------------------

    def export(
        self,
    ) -> List[dict]:
        """
        Export candidate pairs.
        """

        exported = []

        for pair in self._pairs.values():

            exported.append(
                {
                    "left_index": pair.left_index,
                    "right_index": pair.right_index,
                    "match_count": pair.match_count,
                    "block_keys": sorted(
                        pair.block_keys
                    ),
                }
            )

        return exported

    # -----------------------------------------------------
    # Pair Matrix
    # -----------------------------------------------------

    def pair_matrix(
        self,
    ) -> List[Tuple[int, int]]:
        """
        Export normalized pair matrix.
        """

        return [
            (
                pair.left_index,
                pair.right_index,
            )
            for pair in self._pairs.values()
        ]

    # -----------------------------------------------------
    # Strategy Frequency
    # -----------------------------------------------------

    def strategy_frequency(
        self,
    ) -> Dict[str, int]:
        """
        Count how many candidate pairs each
        blocking strategy contributed to.
        """

        frequency: Dict[str, int] = {}

        for pair in self._pairs.values():

            for strategy in pair.block_keys:

                frequency[strategy] = (
                    frequency.get(strategy, 0) + 1
                )

        return dict(
            sorted(
                frequency.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )
        
        # -----------------------------------------------------
    # Candidate Dictionary
    # -----------------------------------------------------

    def to_dict(self) -> Dict[Tuple[int, int], CandidatePair]:
        """
        Return the internal candidate dictionary.
        """

        return dict(self._pairs)

    # -----------------------------------------------------
    # Candidate List
    # -----------------------------------------------------

    def to_list(self) -> List[CandidatePair]:
        """
        Return all candidate pairs.
        """

        return list(self._pairs.values())

    # -----------------------------------------------------
    # Candidate Count by Weight
    # -----------------------------------------------------

    def count_by_weight(
        self,
        weight: int,
    ) -> int:
        """
        Number of candidate pairs having the
        specified blocking weight.
        """

        return sum(
            1
            for pair in self._pairs.values()
            if pair.match_count == weight
        )

    # -----------------------------------------------------
    # Strong Candidates
    # -----------------------------------------------------

    def strong_candidates(
        self,
        minimum_weight: int = 2,
    ) -> List[CandidatePair]:
        """
        Candidates supported by multiple
        blocking strategies.
        """

        return [
            pair
            for pair in self._pairs.values()
            if pair.match_count >= minimum_weight
        ]

    # -----------------------------------------------------
    # Weak Candidates
    # -----------------------------------------------------

    def weak_candidates(
        self,
        maximum_weight: int = 1,
    ) -> List[CandidatePair]:
        """
        Candidates supported by only a few
        blocking strategies.
        """

        return [
            pair
            for pair in self._pairs.values()
            if pair.match_count <= maximum_weight
        ]

    # -----------------------------------------------------
    # Remove Candidate
    # -----------------------------------------------------

    def remove(
        self,
        left: int,
        right: int,
    ) -> bool:
        """
        Remove a candidate pair.

        Returns
        -------
        True if removed.
        """

        key = self.normalize_pair(
            left,
            right,
        )

        if key not in self._pairs:
            return False

        del self._pairs[key]

        return True

    # -----------------------------------------------------
    # Merge Generator
    # -----------------------------------------------------

    def merge(
        self,
        other: "CandidateGenerator",
    ) -> None:
        """
        Merge another generator into this one.
        """

        for pair in other:

            key = pair.pair

            if key not in self._pairs:

                self._pairs[key] = pair

            else:

                self._pairs[key].block_keys.update(
                    pair.block_keys
                )

                self._pairs[key].match_count = len(
                    self._pairs[key].block_keys
                )

    # -----------------------------------------------------
    # Iterator
    # -----------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[CandidatePair]:

        return iter(
            self._pairs.values()
        )

    # -----------------------------------------------------
    # Length
    # -----------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self._pairs)

    # -----------------------------------------------------
    # Contains
    # -----------------------------------------------------

    def __contains__(
        self,
        item: Tuple[int, int],
    ) -> bool:

        if not isinstance(item, tuple):

            return False

        if len(item) != 2:

            return False

        return self.exists(
            item[0],
            item[1],
        )

    # -----------------------------------------------------
    # String Representation
    # -----------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"CandidateGenerator("
            f"pairs={len(self)}, "
            f"processed_blocks={self.statistics.processed_blocks}, "
            f"duplicates={self.statistics.duplicate_pairs})"
        )