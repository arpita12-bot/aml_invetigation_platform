"""
==========================================================
AML Investigation Platform

Enterprise Match Persistence Engine

Responsibilities
----------------
✓ Persist entity matches
✓ Avoid duplicate mappings
✓ Save manual review queue
✓ Maintain audit history
✓ Support batch persistence
✓ Produce runtime statistics
==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from sqlalchemy.orm import Session

from app.entity_resolution.services.confidence_engine import (
    ConfidenceDecision,
    ConfidenceResult,
    ReviewPriority,
)

from app.models.entity_mapping import EntityMapping
from app.models.entity_review_queue import EntityReviewQueue


# ==========================================================
# Configuration
# ==========================================================

@dataclass(slots=True)
class PersistenceConfiguration:
    """
    Persistence configuration.
    """

    save_auto_match: bool = True

    save_manual_review: bool = True

    save_no_match: bool = False

    commit_every: int = 500

    update_existing: bool = True


# ==========================================================
# Runtime Statistics
# ==========================================================

@dataclass(slots=True)
class PersistenceStatistics:
    """
    Runtime persistence statistics.
    """

    processed: int = 0

    inserted: int = 0

    updated: int = 0

    skipped: int = 0

    review_queue: int = 0

    duplicates: int = 0

    errors: int = 0


# ==========================================================
# Match Persistence Engine
# ==========================================================

class MatchPersistenceEngine:
    """
    Enterprise persistence engine.
    """

    def __init__(
        self,
        session: Session,
        config: Optional[
            PersistenceConfiguration
        ] = None,
    ) -> None:

        self.session = session

        self.config = (
            config
            or
            PersistenceConfiguration()
        )

        self.statistics = (
            PersistenceStatistics()
        )

        self.validate_configuration()

    # -----------------------------------------------------
    # Configuration
    # -----------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:

        if self.config.commit_every <= 0:

            raise ValueError(
                "commit_every must be positive."
            )

    # -----------------------------------------------------
    # Reset Statistics
    # -----------------------------------------------------

    def reset(
        self,
    ) -> None:

        self.statistics = (
            PersistenceStatistics()
        )

    # -----------------------------------------------------
    # Update Runtime Statistics
    # -----------------------------------------------------

    def update_statistics(
        self,
        action: str,
    ) -> None:

        self.statistics.processed += 1

        if action == "insert":
            self.statistics.inserted += 1

        elif action == "update":
            self.statistics.updated += 1

        elif action == "duplicate":
            self.statistics.duplicates += 1

        elif action == "review":
            self.statistics.review_queue += 1

        elif action == "skip":
            self.statistics.skipped += 1

        elif action == "error":
            self.statistics.errors += 1
            
        # -----------------------------------------------------
    # Exists
    # -----------------------------------------------------

    def exists(
        self,
        left_index: int,
        right_index: int,
    ) -> bool:
        """
        Check whether a mapping already exists.
        """

        return (

            self.session.query(EntityMapping)

            .filter(
                EntityMapping.left_index == left_index,
                EntityMapping.right_index == right_index,
            )

            .first()

            is not None

        )

    # -----------------------------------------------------
    # Get Existing Match
    # -----------------------------------------------------

    def get_existing_match(
        self,
        left_index: int,
        right_index: int,
    ) -> Optional[EntityMapping]:
        """
        Retrieve an existing mapping.
        """

        return (

            self.session.query(EntityMapping)

            .filter(
                EntityMapping.left_index == left_index,
                EntityMapping.right_index == right_index,
            )

            .first()

        )

    # -----------------------------------------------------
    # Create Mapping
    # -----------------------------------------------------

    def create_mapping(
        self,
        result: ConfidenceResult,
    ) -> EntityMapping:
        """
        Build a new EntityMapping object.
        """

        mapping = EntityMapping(

            left_index=result.left_index,

            right_index=result.right_index,

            similarity_score=result.similarity_score,

            confidence_score=result.confidence_score,

            decision=result.decision.value,

            review_priority=result.priority.value,

            status="ACTIVE",

            metadata=result.metadata,

            created_at=datetime.utcnow(),

            updated_at=datetime.utcnow(),

        )

        return mapping

    # -----------------------------------------------------
    # Update Mapping
    # -----------------------------------------------------

    def update_mapping(
        self,
        mapping: EntityMapping,
        result: ConfidenceResult,
    ) -> EntityMapping:
        """
        Update an existing mapping.
        """

        mapping.similarity_score = result.similarity_score

        mapping.confidence_score = result.confidence_score

        mapping.decision = result.decision.value

        mapping.review_priority = result.priority.value

        mapping.metadata = result.metadata

        mapping.updated_at = datetime.utcnow()

        return mapping

    # -----------------------------------------------------
    # Save Match
    # -----------------------------------------------------

    def save_match(
        self,
        result: ConfidenceResult,
        commit: bool = False,
    ) -> Optional[EntityMapping]:
        """
        Persist a single confidence result.
        """

        try:

            # Skip NO_MATCH if configured
            if (
                result.decision
                ==
                ConfidenceDecision.NO_MATCH
                and
                not self.config.save_no_match
            ):

                self.update_statistics("skip")

                return None

            existing = self.get_existing_match(

                result.left_index,

                result.right_index,

            )

            if existing:

                if not self.config.update_existing:

                    self.update_statistics(
                        "duplicate"
                    )

                    return existing

                existing = self.update_mapping(

                    existing,

                    result,

                )

                self.update_statistics(
                    "update"
                )

                if commit:
                    self.session.commit()

                return existing

            mapping = self.create_mapping(
                result
            )

            self.session.add(mapping)

            self.update_statistics(
                "insert"
            )

            if commit:
                self.session.commit()

            return mapping

        except Exception:

            self.session.rollback()

            self.update_statistics(
                "error"
            )

            raise

    # -----------------------------------------------------
    # Save Batch
    # -----------------------------------------------------

    def save_batch(
        self,
        results: Iterable[ConfidenceResult],
        commit: bool = True,
    ) -> List[EntityMapping]:
        """
        Persist multiple matches.
        """

        persisted: List[
            EntityMapping
        ] = []

        counter = 0

        try:

            for result in results:

                mapping = self.save_match(
                    result,
                    commit=False,
                )

                if mapping is not None:

                    persisted.append(
                        mapping
                    )

                counter += 1

                if (
                    counter
                    %
                    self.config.commit_every
                    ==
                    0
                ):

                    self.session.commit()

            if commit:

                self.session.commit()

            return persisted

        except Exception:

            self.session.rollback()

            self.update_statistics(
                "error"
            )

            raise
        
        # -----------------------------------------------------
    # Is In Review Queue
    # -----------------------------------------------------

    def is_in_review_queue(
        self,
        left_index: int,
        right_index: int,
    ) -> bool:
        """
        Check whether a pair is already queued.
        """

        return (

            self.session.query(EntityReviewQueue)

            .filter(
                EntityReviewQueue.left_index == left_index,
                EntityReviewQueue.right_index == right_index,
            )

            .first()

            is not None

        )

    # -----------------------------------------------------
    # Enqueue Review
    # -----------------------------------------------------

    def enqueue_review(
        self,
        mapping: EntityMapping,
        result: ConfidenceResult,
        commit: bool = False,
    ) -> Optional[EntityReviewQueue]:
        """
        Add a match to the manual review queue.
        """

        if (
            result.decision
            !=
            ConfidenceDecision.MANUAL_REVIEW
        ):
            return None

        if self.is_in_review_queue(

            result.left_index,

            result.right_index,

        ):

            self.update_statistics(
                "duplicate"
            )

            return None

        review = EntityReviewQueue(

            mapping_id=getattr(
                mapping,
                "id",
                None,
            ),

            left_index=result.left_index,

            right_index=result.right_index,

            confidence_score=result.confidence_score,

            priority=result.priority.value,

            status="PENDING",

            assigned_to=None,

            review_notes=None,

            created_at=datetime.utcnow(),

            updated_at=datetime.utcnow(),

        )

        self.session.add(review)

        self.update_statistics(
            "review"
        )

        if commit:
            self.session.commit()

        return review

    # -----------------------------------------------------
    # Remove From Review Queue
    # -----------------------------------------------------

    def remove_from_review_queue(
        self,
        review_id: int,
        commit: bool = True,
    ) -> bool:
        """
        Remove a review queue entry.
        """

        review = (

            self.session.query(
                EntityReviewQueue
            )

            .filter(
                EntityReviewQueue.id == review_id
            )

            .first()

        )

        if review is None:
            return False

        self.session.delete(review)

        if commit:
            self.session.commit()

        return True

    # -----------------------------------------------------
    # Assign Reviewer
    # -----------------------------------------------------

    def assign_reviewer(
        self,
        review_id: int,
        reviewer: str,
        commit: bool = True,
    ) -> Optional[EntityReviewQueue]:
        """
        Assign an AML analyst.
        """

        review = (

            self.session.query(
                EntityReviewQueue
            )

            .filter(
                EntityReviewQueue.id == review_id
            )

            .first()

        )

        if review is None:
            return None

        review.assigned_to = reviewer

        review.updated_at = datetime.utcnow()

        if commit:
            self.session.commit()

        return review

    # -----------------------------------------------------
    # Update Review Status
    # -----------------------------------------------------

    def update_review_status(
        self,
        review_id: int,
        status: str,
        notes: Optional[str] = None,
        commit: bool = True,
    ) -> Optional[EntityReviewQueue]:
        """
        Update review workflow status.
        """

        review = (

            self.session.query(
                EntityReviewQueue
            )

            .filter(
                EntityReviewQueue.id == review_id
            )

            .first()

        )

        if review is None:
            return None

        review.status = status

        review.review_notes = notes

        review.updated_at = datetime.utcnow()

        if commit:
            self.session.commit()

        return review

    # -----------------------------------------------------
    # Pending Reviews
    # -----------------------------------------------------

    def pending_reviews(
        self,
    ) -> List[EntityReviewQueue]:
        """
        Retrieve pending reviews.
        """

        return (

            self.session.query(
                EntityReviewQueue
            )

            .filter(
                EntityReviewQueue.status == "PENDING"
            )

            .all()

        )

    # -----------------------------------------------------
    # Review Statistics
    # -----------------------------------------------------

    def review_statistics(
        self,
    ) -> Dict[str, int]:
        """
        Manual review queue statistics.
        """

        pending = (

            self.session.query(
                EntityReviewQueue
            )

            .filter(
                EntityReviewQueue.status == "PENDING"
            )

            .count()

        )

        completed = (

            self.session.query(
                EntityReviewQueue
            )

            .filter(
                EntityReviewQueue.status == "COMPLETED"
            )

            .count()

        )

        assigned = (

            self.session.query(
                EntityReviewQueue
            )

            .filter(
                EntityReviewQueue.assigned_to.isnot(None)
            )

            .count()

        )

        return {

            "pending": pending,

            "completed": completed,

            "assigned": assigned,

            "total": pending + completed,

        }
        # -----------------------------------------------------
    # Bulk Insert
    # -----------------------------------------------------

    def bulk_insert(
        self,
        results: Iterable[ConfidenceResult],
        commit: bool = True,
    ) -> List[EntityMapping]:
        """
        Insert multiple mappings efficiently.
        """

        mappings: List[EntityMapping] = []

        try:

            for result in results:

                if (
                    result.decision ==
                    ConfidenceDecision.NO_MATCH
                    and
                    not self.config.save_no_match
                ):
                    self.update_statistics("skip")
                    continue

                if self.exists(
                    result.left_index,
                    result.right_index,
                ):
                    self.update_statistics("duplicate")
                    continue

                mapping = self.create_mapping(result)

                mappings.append(mapping)

            if mappings:

                self.session.bulk_save_objects(
                    mappings,
                )

                self.statistics.inserted += len(
                    mappings
                )

                self.statistics.processed += len(
                    mappings
                )

            if commit:
                self.session.commit()

            return mappings

        except Exception:

            self.session.rollback()

            self.update_statistics("error")

            raise

    # -----------------------------------------------------
    # Bulk Update
    # -----------------------------------------------------

    def bulk_update(
        self,
        results: Iterable[ConfidenceResult],
        commit: bool = True,
    ) -> int:
        """
        Update existing mappings.
        """

        updated = 0

        try:

            for result in results:

                mapping = self.get_existing_match(
                    result.left_index,
                    result.right_index,
                )

                if mapping is None:
                    continue

                self.update_mapping(
                    mapping,
                    result,
                )

                updated += 1

            self.statistics.updated += updated

            self.statistics.processed += updated

            if commit:
                self.session.commit()

            return updated

        except Exception:

            self.session.rollback()

            self.update_statistics("error")

            raise

    # -----------------------------------------------------
    # Stream Persistence
    # -----------------------------------------------------

    def stream_persistence(
        self,
        results: Iterable[ConfidenceResult],
    ) -> Iterable[EntityMapping]:
        """
        Persist results lazily.
        """

        counter = 0

        for result in results:

            mapping = self.save_match(
                result,
                commit=False,
            )

            if mapping is not None:

                yield mapping

            counter += 1

            if (
                counter %
                self.config.commit_every
                ==
                0
            ):
                self.session.commit()

        self.session.commit()

    # -----------------------------------------------------
    # Batch Iterator
    # -----------------------------------------------------

    def batch_iterator(
        self,
        results: Iterable[ConfidenceResult],
        batch_size: int = 1000,
    ) -> Iterable[List[ConfidenceResult]]:
        """
        Yield batches of confidence results.
        """

        batch: List[
            ConfidenceResult
        ] = []

        for result in results:

            batch.append(result)

            if len(batch) >= batch_size:

                yield batch

                batch = []

        if batch:

            yield batch

    # -----------------------------------------------------
    # Commit
    # -----------------------------------------------------

    def commit(
        self,
    ) -> None:
        """
        Commit current transaction.
        """

        self.session.commit()

    # -----------------------------------------------------
    # Rollback
    # -----------------------------------------------------

    def rollback(
        self,
    ) -> None:
        """
        Rollback current transaction.
        """

        self.session.rollback()

    # -----------------------------------------------------
    # Flush
    # -----------------------------------------------------

    def flush(
        self,
    ) -> None:
        """
        Flush pending SQL operations.
        """

        self.session.flush()

    # -----------------------------------------------------
    # Refresh
    # -----------------------------------------------------

    def refresh(
        self,
        mapping: EntityMapping,
    ) -> EntityMapping:
        """
        Refresh entity from database.
        """

        self.session.refresh(
            mapping,
        )

        return mapping

    # -----------------------------------------------------
    # Delete Mapping
    # -----------------------------------------------------

    def delete_mapping(
        self,
        mapping_id: int,
        commit: bool = True,
    ) -> bool:
        """
        Delete a persisted mapping.
        """

        mapping = (

            self.session.query(
                EntityMapping
            )

            .filter(
                EntityMapping.id == mapping_id
            )

            .first()

        )

        if mapping is None:
            return False

        self.session.delete(mapping)

        if commit:
            self.session.commit()

        return True

    # -----------------------------------------------------
    # Count Persisted Mappings
    # -----------------------------------------------------

    def mapping_count(
        self,
    ) -> int:
        """
        Total persisted mappings.
        """

        return (

            self.session.query(
                EntityMapping
            )

            .count()

        )
        # -----------------------------------------------------
    # Statistics Report
    # -----------------------------------------------------

    def statistics_report(
        self,
    ) -> Dict[str, Any]:
        """
        Return runtime persistence statistics.
        """

        stats = self.statistics

        return {

            "processed": stats.processed,

            "inserted": stats.inserted,

            "updated": stats.updated,

            "duplicates": stats.duplicates,

            "review_queue": stats.review_queue,

            "skipped": stats.skipped,

            "errors": stats.errors,
        }

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    def metrics(
        self,
    ) -> Dict[str, Any]:
        """
        Calculate persistence metrics.
        """

        stats = self.statistics

        processed = max(
            stats.processed,
            1,
        )

        return {

            "insert_rate":
                round(
                    stats.inserted / processed,
                    4,
                ),

            "update_rate":
                round(
                    stats.updated / processed,
                    4,
                ),

            "duplicate_rate":
                round(
                    stats.duplicates / processed,
                    4,
                ),

            "review_rate":
                round(
                    stats.review_queue / processed,
                    4,
                ),

            "skip_rate":
                round(
                    stats.skipped / processed,
                    4,
                ),

            "error_rate":
                round(
                    stats.errors / processed,
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
        Persistence engine health.
        """

        return {

            "status": "healthy",

            "engine":
                self.__class__.__name__,

            "database_connected":
                self.session.is_active,

            "processed_records":
                self.statistics.processed,

            "total_mappings":
                self.mapping_count(),

            "review_queue":
                self.review_statistics(),
        }

    # -----------------------------------------------------
    # Configuration
    # -----------------------------------------------------

    def configuration(
        self,
    ) -> Dict[str, Any]:
        """
        Active persistence configuration.
        """

        cfg = self.config

        return {

            "save_auto_match":
                cfg.save_auto_match,

            "save_manual_review":
                cfg.save_manual_review,

            "save_no_match":
                cfg.save_no_match,

            "commit_every":
                cfg.commit_every,

            "update_existing":
                cfg.update_existing,
        }

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Complete engine summary.
        """

        return {

            "health":
                self.health_check(),

            "configuration":
                self.configuration(),

            "statistics":
                self.statistics_report(),

            "metrics":
                self.metrics(),
        }

    # -----------------------------------------------------
    # Export Mapping
    # -----------------------------------------------------

    def export(
        self,
        mapping: EntityMapping,
    ) -> Dict[str, Any]:
        """
        Export EntityMapping.
        """

        return {

            "id":
                getattr(mapping, "id", None),

            "left_index":
                mapping.left_index,

            "right_index":
                mapping.right_index,

            "similarity_score":
                mapping.similarity_score,

            "confidence_score":
                mapping.confidence_score,

            "decision":
                mapping.decision,

            "review_priority":
                mapping.review_priority,

            "status":
                mapping.status,

            "metadata":
                mapping.metadata,

            "created_at":
                mapping.created_at,

            "updated_at":
                mapping.updated_at,
        }

    # -----------------------------------------------------
    # Export Batch
    # -----------------------------------------------------

    def export_batch(
        self,
        mappings: Iterable[
            EntityMapping
        ],
    ) -> List[
        Dict[str, Any]
    ]:
        """
        Export multiple mappings.
        """

        return [

            self.export(mapping)

            for mapping in mappings

        ]

    # -----------------------------------------------------
    # Runtime Snapshot
    # -----------------------------------------------------

    def runtime_snapshot(
        self,
    ) -> Dict[str, Any]:
        """
        Current runtime state.
        """

        return {

            "statistics":
                self.statistics_report(),

            "metrics":
                self.metrics(),

            "review_statistics":
                self.review_statistics(),

            "configuration":
                self.configuration(),
        }

    # -----------------------------------------------------
    # Print Summary
    # -----------------------------------------------------

    def print_summary(
        self,
    ) -> None:
        """
        Print persistence summary.
        """

        summary = self.summary()

        print("=" * 60)
        print("Match Persistence Engine")
        print("=" * 60)

        print()

        print("Health")
        print("------")

        for key, value in summary["health"].items():
            print(f"{key}: {value}")

        print()

        print("Statistics")
        print("----------")

        for key, value in summary["statistics"].items():
            print(f"{key}: {value}")

        print()

        print("Metrics")
        print("-------")

        for key, value in summary["metrics"].items():
            print(f"{key}: {value}")
            
        # -----------------------------------------------------
    # Find Mapping
    # -----------------------------------------------------

    def find_mapping(
        self,
        mapping_id: int,
    ) -> Optional[EntityMapping]:
        """
        Find mapping by ID.
        """

        return (
            self.session.query(EntityMapping)
            .filter(
                EntityMapping.id == mapping_id
            )
            .first()
        )

    # -----------------------------------------------------
    # Find By Decision
    # -----------------------------------------------------

    def find_by_decision(
        self,
        decision: ConfidenceDecision,
    ) -> List[EntityMapping]:
        """
        Find mappings by decision.
        """

        return (
            self.session.query(EntityMapping)
            .filter(
                EntityMapping.decision == decision.value
            )
            .all()
        )

    # -----------------------------------------------------
    # Find By Priority
    # -----------------------------------------------------

    def find_by_priority(
        self,
        priority: ReviewPriority,
    ) -> List[EntityMapping]:
        """
        Find mappings by review priority.
        """

        return (
            self.session.query(EntityMapping)
            .filter(
                EntityMapping.review_priority == priority.value
            )
            .all()
        )

    # -----------------------------------------------------
    # Find Pending Reviews
    # -----------------------------------------------------

    def find_pending_reviews(
        self,
    ) -> List[EntityReviewQueue]:
        """
        Retrieve all pending reviews.
        """

        return (
            self.session.query(EntityReviewQueue)
            .filter(
                EntityReviewQueue.status == "PENDING"
            )
            .order_by(
                EntityReviewQueue.created_at.asc()
            )
            .all()
        )

    # -----------------------------------------------------
    # Cleanup Duplicate Queue Entries
    # -----------------------------------------------------

    def cleanup_duplicates(
        self,
        commit: bool = True,
    ) -> int:
        """
        Remove duplicate review queue entries.

        Keeps the oldest record for each
        (left_index, right_index) pair.
        """

        removed = 0

        reviews = (
            self.session.query(EntityReviewQueue)
            .order_by(
                EntityReviewQueue.created_at.asc()
            )
            .all()
        )

        seen = set()

        for review in reviews:

            key = (
                review.left_index,
                review.right_index,
            )

            if key in seen:

                self.session.delete(review)

                removed += 1

            else:

                seen.add(key)

        if commit:
            self.session.commit()

        return removed

    # -----------------------------------------------------
    # Archive Mapping
    # -----------------------------------------------------

    def archive_mapping(
        self,
        mapping_id: int,
        commit: bool = True,
    ) -> Optional[EntityMapping]:
        """
        Archive a mapping.
        """

        mapping = self.find_mapping(
            mapping_id,
        )

        if mapping is None:
            return None

        mapping.status = "ARCHIVED"

        mapping.updated_at = datetime.utcnow()

        if commit:
            self.session.commit()

        return mapping

    # -----------------------------------------------------
    # Active Mapping Count
    # -----------------------------------------------------

    def active_mapping_count(
        self,
    ) -> int:
        """
        Count active mappings.
        """

        return (
            self.session.query(EntityMapping)
            .filter(
                EntityMapping.status == "ACTIVE"
            )
            .count()
        )

    # -----------------------------------------------------
    # Pending Review Count
    # -----------------------------------------------------

    def pending_review_count(
        self,
    ) -> int:
        """
        Count pending reviews.
        """

        return (
            self.session.query(EntityReviewQueue)
            .filter(
                EntityReviewQueue.status == "PENDING"
            )
            .count()
        )

    # -----------------------------------------------------
    # Length
    # -----------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Number of processed records.
        """

        return self.statistics.processed

    # -----------------------------------------------------
    # Boolean
    # -----------------------------------------------------

    def __bool__(
        self,
    ) -> bool:
        """
        True if any records have been processed.
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
            f"inserted={self.statistics.inserted}, "
            f"updated={self.statistics.updated}, "
            f"errors={self.statistics.errors})"
        )

    # -----------------------------------------------------
    # String Representation
    # -----------------------------------------------------

    def __str__(
        self,
    ) -> str:
        """
        User-friendly summary.
        """

        return (
            f"MatchPersistenceEngine"
            f"[processed={self.statistics.processed}, "
            f"inserted={self.statistics.inserted}, "
            f"updated={self.statistics.updated}, "
            f"duplicates={self.statistics.duplicates}, "
            f"review_queue={self.statistics.review_queue}]"
        )