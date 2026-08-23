"""
==========================================================

AML Investigation Platform

Enterprise Blocking Engine

Responsibilities
----------------
✓ Generate blocking keys
✓ Build candidate blocks
✓ Apply multiple blocking strategies
✓ Reduce comparison space
✓ Produce blocking metrics

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.utils.blocking_utils import BlockingUtils


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


@dataclass
class BlockingConfiguration:

    enable_country: bool = True

    enable_name: bool = True

    enable_phone: bool = True

    enable_email: bool = True

    enable_company: bool = True

    enable_composite: bool = True

    minimum_block_size: int = 2

    maximum_block_size: int = 500


# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------


@dataclass
class BlockingMetrics:

    total_records: int = 0

    total_blocks: int = 0

    average_block_size: float = 0.0

    largest_block_size: int = 0

    largest_block_key: str = ""

    singleton_blocks: int = 0

    filtered_blocks: int = 0


# ---------------------------------------------------------
# Blocking Engine
# ---------------------------------------------------------


class BlockingEngine:

    """
    Enterprise Blocking Engine.
    """

    def __init__(
        self,
        config: Optional[BlockingConfiguration] = None,
    ):

        self.config = config or BlockingConfiguration()

        self.blocks: Dict[str, List[int]] = {}

        self.metrics = BlockingMetrics()

    # -----------------------------------------------------
    # Reset
    # -----------------------------------------------------

    def reset(self):

        self.blocks.clear()

        self.metrics = BlockingMetrics()

    # -----------------------------------------------------
    # Build Keys
    # -----------------------------------------------------

    def build_keys(
        self,
        record: dict,
    ) -> List[str]:

        keys = []

        generated = BlockingUtils.build_multiple_keys(
            name=record.get("name"),
            country=record.get("country"),
            dob=record.get("dob"),
            postal_code=record.get("postal_code"),
            city=record.get("city"),
            phone=record.get("phone"),
            email=record.get("email"),
            company=record.get("company"),
        )

        for key in generated:

            if not key:
                continue

            keys.append(key)

        return BlockingUtils.unique_keys(keys)

    # -----------------------------------------------------
    # Add Record
    # -----------------------------------------------------

    def add_record(
        self,
        index: int,
        record: dict,
    ):

        keys = self.build_keys(record)

        for key in keys:

            self.blocks.setdefault(key, []).append(index)
            
            
        # -----------------------------------------------------
    # Build Blocks
    # -----------------------------------------------------

    def build_blocks(
        self,
        records: List[dict],
    ) -> Dict[str, List[int]]:
        """
        Build blocking index for all records.
        """

        self.reset()

        self.metrics.total_records = len(records)

        for index, record in enumerate(records):
            self.add_record(index, record)

        self.filter_small_blocks()
        self.filter_large_blocks()
        self.compute_metrics()

        return self.blocks

    # -----------------------------------------------------
    # Filter Small Blocks
    # -----------------------------------------------------

    def filter_small_blocks(self):
        """
        Remove blocks containing fewer than
        the configured minimum number of members.
        """

        removed = 0

        filtered = {}

        for key, members in self.blocks.items():

            if len(members) < self.config.minimum_block_size:
                removed += 1
                continue

            filtered[key] = members

        self.blocks = filtered

        self.metrics.filtered_blocks += removed

    # -----------------------------------------------------
    # Filter Large Blocks
    # -----------------------------------------------------

    def filter_large_blocks(self):
        """
        Remove overly large blocks because
        they usually produce excessive
        comparisons.
        """

        removed = 0

        filtered = {}

        for key, members in self.blocks.items():

            if len(members) > self.config.maximum_block_size:
                removed += 1
                continue

            filtered[key] = members

        self.blocks = filtered

        self.metrics.filtered_blocks += removed

    # -----------------------------------------------------
    # Sorted Blocks
    # -----------------------------------------------------

    def sorted_blocks(
        self
    ) -> List[tuple[str, List[int]]]:
        """
        Largest blocks first.
        """

        return sorted(
            self.blocks.items(),
            key=lambda x: len(x[1]),
            reverse=True,
        )

    # -----------------------------------------------------
    # Block Sizes
    # -----------------------------------------------------

    def block_sizes(self) -> Dict[str, int]:

        return {
            key: len(value)
            for key, value in self.blocks.items()
        }

    # -----------------------------------------------------
    # Compute Metrics
    # -----------------------------------------------------

    def compute_metrics(self):

        self.metrics.total_blocks = len(self.blocks)

        if not self.blocks:
            return

        sizes = [
            len(v)
            for v in self.blocks.values()
        ]

        self.metrics.average_block_size = (
            sum(sizes) / len(sizes)
        )

        largest_key = max(
            self.blocks,
            key=lambda x: len(self.blocks[x]),
        )

        self.metrics.largest_block_key = largest_key

        self.metrics.largest_block_size = len(
            self.blocks[largest_key]
        )

        self.metrics.singleton_blocks = sum(
            1
            for members in self.blocks.values()
            if len(members) == 1
        )

    # -----------------------------------------------------
    # Get Block
    # -----------------------------------------------------

    def get_block(
        self,
        key: str,
    ) -> List[int]:

        return self.blocks.get(key, [])

    # -----------------------------------------------------
    # Block Exists
    # -----------------------------------------------------

    def has_block(
        self,
        key: str,
    ) -> bool:

        return key in self.blocks

    # -----------------------------------------------------
    # Total Candidates
    # -----------------------------------------------------

    def total_candidates(self) -> int:
        """
        Total records contained in all blocks.
        """

        return sum(
            len(block)
            for block in self.blocks.values()
        )
        
        
        # -----------------------------------------------------
    # Update Record
    # -----------------------------------------------------

    def update_record(
        self,
        index: int,
        old_record: dict,
        new_record: dict,
    ) -> None:
        """
        Update an existing record by removing its old
        blocking keys and inserting the new ones.
        """

        self.remove_record(index, old_record)

        self.add_record(index, new_record)

    # -----------------------------------------------------
    # Remove Record
    # -----------------------------------------------------

    def remove_record(
        self,
        index: int,
        record: dict,
    ) -> None:
        """
        Remove a record from every block it belongs to.
        """

        keys = self.build_keys(record)

        for key in keys:

            if key not in self.blocks:
                continue

            if index in self.blocks[key]:
                self.blocks[key].remove(index)

            if not self.blocks[key]:
                del self.blocks[key]

    # -----------------------------------------------------
    # Candidate Records
    # -----------------------------------------------------

    def candidate_indexes(
        self,
        record: dict,
    ) -> List[int]:
        """
        Return all candidate record indexes
        belonging to the same blocks.
        """

        candidates = set()

        keys = self.build_keys(record)

        for key in keys:

            members = self.blocks.get(key, [])

            candidates.update(members)

        return sorted(candidates)

    # -----------------------------------------------------
    # Candidate Blocks
    # -----------------------------------------------------

    def candidate_blocks(
        self,
        record: dict,
    ) -> Dict[str, List[int]]:
        """
        Return every block associated with
        a given record.
        """

        result = {}

        keys = self.build_keys(record)

        for key in keys:

            if key in self.blocks:
                result[key] = self.blocks[key]

        return result

    # -----------------------------------------------------
    # Merge Blocks
    # -----------------------------------------------------

    def merge_blocks(
        self,
        primary_key: str,
        secondary_key: str,
    ) -> None:
        """
        Merge two existing blocks.
        """

        if primary_key not in self.blocks:
            return

        if secondary_key not in self.blocks:
            return

        merged = set(self.blocks[primary_key])

        merged.update(self.blocks[secondary_key])

        self.blocks[primary_key] = sorted(merged)

        del self.blocks[secondary_key]

    # -----------------------------------------------------
    # Split Large Block
    # -----------------------------------------------------

    def split_large_block(
        self,
        key: str,
        chunk_size: int = 100,
    ) -> None:
        """
        Split an oversized block into
        smaller logical chunks.

        Example

        BLOCK_A

        →

        BLOCK_A_1
        BLOCK_A_2
        BLOCK_A_3
        """

        if key not in self.blocks:
            return

        members = self.blocks[key]

        if len(members) <= chunk_size:
            return

        del self.blocks[key]

        for start in range(0, len(members), chunk_size):

            end = start + chunk_size

            new_key = f"{key}_{start // chunk_size + 1}"

            self.blocks[new_key] = members[start:end]

    # -----------------------------------------------------
    # Incremental Build
    # -----------------------------------------------------

    def incremental_build(
        self,
        records: List[dict],
        starting_index: int,
    ) -> None:
        """
        Add newly ingested records without
        rebuilding the entire blocking index.
        """

        for offset, record in enumerate(records):

            self.add_record(
                starting_index + offset,
                record,
            )

        self.compute_metrics()

    # -----------------------------------------------------
    # Clear Empty Blocks
    # -----------------------------------------------------

    def clear_empty_blocks(self) -> None:
        """
        Remove empty block entries.
        """

        self.blocks = {
            key: members
            for key, members in self.blocks.items()
            if members
        }

    # -----------------------------------------------------
    # Refresh Metrics
    # -----------------------------------------------------

    def refresh(self) -> None:
        """
        Refresh metrics after incremental updates.
        """

        self.clear_empty_blocks()

        self.compute_metrics()
        
        # -----------------------------------------------------
    # Batch Processing
    # -----------------------------------------------------

    def process_batch(
        self,
        records: List[dict],
        batch_size: int = 1000,
    ) -> None:
        """
        Process records in batches to reduce
        memory consumption.

        Suitable for datasets containing
        millions of records.
        """

        self.reset()

        total = len(records)

        self.metrics.total_records = total

        for start in range(0, total, batch_size):

            end = min(start + batch_size, total)

            batch = records[start:end]

            for offset, record in enumerate(batch):

                self.add_record(
                    start + offset,
                    record,
                )

        self.filter_small_blocks()

        self.filter_large_blocks()

        self.compute_metrics()

    # -----------------------------------------------------
    # Reduction Ratio
    # -----------------------------------------------------

    def reduction_ratio(self) -> float:
        """
        Calculate comparison reduction.

        RR = 1 - candidate_pairs /
                 total_possible_pairs
        """

        n = self.metrics.total_records

        if n <= 1:
            return 1.0

        total_pairs = (n * (n - 1)) / 2

        candidate_pairs = 0

        for members in self.blocks.values():

            m = len(members)

            candidate_pairs += (m * (m - 1)) / 2

        return max(
            0.0,
            1 - (candidate_pairs / total_pairs),
        )

    # -----------------------------------------------------
    # Candidate Pair Estimate
    # -----------------------------------------------------

    def candidate_pair_count(self) -> int:
        """
        Number of pairwise comparisons
        after blocking.
        """

        total = 0

        for members in self.blocks.values():

            n = len(members)

            total += (n * (n - 1)) // 2

        return total

    # -----------------------------------------------------
    # Average Candidates
    # -----------------------------------------------------

    def average_candidates(self) -> float:

        if self.metrics.total_blocks == 0:
            return 0.0

        return (
            self.total_candidates()
            /
            self.metrics.total_blocks
        )

    # -----------------------------------------------------
    # Largest Blocks
    # -----------------------------------------------------

    def largest_blocks(
        self,
        top_n: int = 10,
    ) -> List[tuple[str, int]]:

        return [
            (
                key,
                len(members),
            )
            for key, members
            in sorted(
                self.blocks.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )[:top_n]
        ]

    # -----------------------------------------------------
    # Block Density
    # -----------------------------------------------------

    def block_density(self) -> float:
        """
        Average density of populated blocks.
        """

        if not self.blocks:
            return 0.0

        populated = sum(
            1
            for members in self.blocks.values()
            if len(members) > 1
        )

        return populated / len(self.blocks)

    # -----------------------------------------------------
    # Empty
    # -----------------------------------------------------

    def is_empty(self) -> bool:

        return len(self.blocks) == 0

    # -----------------------------------------------------
    # Clear
    # -----------------------------------------------------

    def clear(self) -> None:

        self.reset()
        
        # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(self) -> dict:
        """
        Perform a basic health check of the blocking engine.
        """

        return {
            "healthy": not self.is_empty(),
            "total_records": self.metrics.total_records,
            "total_blocks": self.metrics.total_blocks,
            "largest_block_size": self.metrics.largest_block_size,
            "average_block_size": round(
                self.metrics.average_block_size,
                2,
            ),
            "reduction_ratio": round(
                self.reduction_ratio(),
                4,
            ),
        }

    # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    def statistics(self) -> dict:
        """
        Return detailed engine statistics.
        """

        return {
            "records": self.metrics.total_records,
            "blocks": self.metrics.total_blocks,
            "candidate_pairs": self.candidate_pair_count(),
            "average_block_size": round(
                self.metrics.average_block_size,
                2,
            ),
            "largest_block": {
                "key": self.metrics.largest_block_key,
                "size": self.metrics.largest_block_size,
            },
            "singleton_blocks": self.metrics.singleton_blocks,
            "filtered_blocks": self.metrics.filtered_blocks,
            "reduction_ratio": round(
                self.reduction_ratio(),
                4,
            ),
            "density": round(
                self.block_density(),
                4,
            ),
        }

    # -----------------------------------------------------
    # Export Configuration
    # -----------------------------------------------------

    def configuration(self) -> dict:
        """
        Export engine configuration.
        """

        return {
            "enable_country": self.config.enable_country,
            "enable_name": self.config.enable_name,
            "enable_phone": self.config.enable_phone,
            "enable_email": self.config.enable_email,
            "enable_company": self.config.enable_company,
            "enable_composite": self.config.enable_composite,
            "minimum_block_size": self.config.minimum_block_size,
            "maximum_block_size": self.config.maximum_block_size,
        }

    # -----------------------------------------------------
    # Engine Summary
    # -----------------------------------------------------

    def summary(self) -> dict:
        """
        Combined configuration and statistics.
        """

        return {
            "configuration": self.configuration(),
            "statistics": self.statistics(),
            "health": self.health_check(),
        }

    # -----------------------------------------------------
    # Print Summary
    # -----------------------------------------------------

    def print_summary(self) -> None:
        """
        Print engine statistics to the console.
        """

        summary = self.summary()

        print("=" * 60)
        print("Enterprise Blocking Engine Summary")
        print("=" * 60)

        print(f"Records           : {summary['statistics']['records']}")
        print(f"Blocks            : {summary['statistics']['blocks']}")
        print(f"Candidate Pairs   : {summary['statistics']['candidate_pairs']}")
        print(f"Reduction Ratio   : {summary['statistics']['reduction_ratio']}")
        print(f"Largest Block     : {summary['statistics']['largest_block']['size']}")
        print(f"Average Size      : {summary['statistics']['average_block_size']}")
        print(f"Density           : {summary['statistics']['density']}")

        print("=" * 60)

    # -----------------------------------------------------
    # Iterator
    # -----------------------------------------------------

    def __iter__(self):
        """
        Iterate over block dictionary.
        """

        return iter(self.blocks.items())

    # -----------------------------------------------------
    # Length
    # -----------------------------------------------------

    def __len__(self) -> int:

        return len(self.blocks)

    # -----------------------------------------------------
    # String Representation
    # -----------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"BlockingEngine("
            f"records={self.metrics.total_records}, "
            f"blocks={self.metrics.total_blocks}, "
            f"pairs={self.candidate_pair_count()})"
        )