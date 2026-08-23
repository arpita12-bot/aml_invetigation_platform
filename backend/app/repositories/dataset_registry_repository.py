"""
==========================================================
AML Investigation Platform

Dataset Registry Repository
==========================================================
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from sqlalchemy import func, text
from sqlalchemy.orm import Session


from app.models.dataset_registry import DatasetRegistry
from app.core.constants import (
    UploadStatus,
    ValidationStatus,
    ProcessingStatus,
)

logger = logging.getLogger(__name__)


class DatasetRegistryRepository:
    """
    Repository responsible for all Dataset Registry
    database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create_dataset(
        self,
        dataset: DatasetRegistry,
    ) -> DatasetRegistry:
        """
        Register uploaded dataset.
        """

        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)

        logger.info(
            "Dataset registered: %s",
            dataset.dataset_name,
        )

        return dataset

    # -----------------------------------------------------

    def create_from_dict(
        self,
        values: Dict,
    ) -> DatasetRegistry:
        """
        Create dataset registry record from dictionary.
        """

        dataset = DatasetRegistry(**values)

        return self.create_dataset(dataset)

    # =====================================================
    # GET
    # =====================================================

    def get_by_id(
        self,
        dataset_id: int,
    ) -> Optional[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.dataset_id == dataset_id
            )
            .first()
        )

    # -----------------------------------------------------

    def get_by_dataset_name(
        self,
        dataset_name: str,
    ) -> Optional[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.dataset_name == dataset_name
            )
            .first()
        )

    # -----------------------------------------------------

    def get_by_table_name(
        self,
        table_name: str,
    ) -> Optional[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.table_name == table_name
            )
            .first()
        )

    # -----------------------------------------------------

    def get_by_file_hash(
        self,
        file_hash: str,
    ) -> Optional[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.file_hash == file_hash
            )
            .first()
        )

    # -----------------------------------------------------

    def get_by_original_filename(
        self,
        filename: str,
    ) -> Optional[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.original_filename == filename
            )
            .first()
        )

    # -----------------------------------------------------

    def dataset_exists(
        self,
        table_name: str,
    ) -> bool:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.table_name == table_name
            )
            .count()
            > 0
        )

    # -----------------------------------------------------

    def file_already_uploaded(
        self,
        file_hash: str,
    ) -> bool:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.file_hash == file_hash
            )
            .count()
            > 0
        )

    # =====================================================
    # LIST
    # =====================================================

    def list_datasets(
        self,
    ) -> List[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .order_by(
                DatasetRegistry.created_at.desc()
            )
            .all()
        )

    # -----------------------------------------------------

    def list_active_datasets(
        self,
    ) -> List[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.is_active.is_(True)
            )
            .order_by(
                DatasetRegistry.created_at.desc()
            )
            .all()
        )

    # -----------------------------------------------------

    def list_by_dataset_type(
        self,
        dataset_type: str,
    ) -> List[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.dataset_type == dataset_type
            )
            .all()
        )

    # -----------------------------------------------------

    def list_by_upload_status(
        self,
        status: UploadStatus,
    ) -> List[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.upload_status == status
            )
            .all()
        )

    # -----------------------------------------------------

    def list_by_processing_status(
        self,
        status: ProcessingStatus,
    ) -> List[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.processing_status == status
            )
            .all()
        )

    # -----------------------------------------------------

    def recent_uploads(
        self,
        limit: int = 10,
    ) -> List[DatasetRegistry]:

        return (
            self.db.query(DatasetRegistry)
            .order_by(
                DatasetRegistry.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    # -----------------------------------------------------

    def search(
        self,
        keyword: str,
    ) -> List[DatasetRegistry]:

        keyword = f"%{keyword}%"

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.dataset_name.ilike(keyword)
                | DatasetRegistry.original_filename.ilike(keyword)
                | DatasetRegistry.table_name.ilike(keyword)
            )
            .all()
        )
        
    # =====================================================
    # UPDATE
    # =====================================================

    def update_dataset(
        self,
        dataset: DatasetRegistry,
    ) -> DatasetRegistry:
        """
        Persist changes to an existing dataset.
        """

        self.db.commit()
        self.db.refresh(dataset)

        logger.info(
            "Dataset updated: %s",
            dataset.dataset_name,
        )

        return dataset

    # -----------------------------------------------------

    def update_upload_status(
        self,
        dataset_id: int,
        status: UploadStatus,
    ) -> Optional[DatasetRegistry]:
        """
        Update upload status.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.upload_status = status

        return self.update_dataset(dataset)

    # -----------------------------------------------------

    def update_validation_status(
        self,
        dataset_id: int,
        status: ValidationStatus,
    ) -> Optional[DatasetRegistry]:
        """
        Update validation status.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.validation_status = status

        return self.update_dataset(dataset)

    # -----------------------------------------------------

    def update_processing_status(
        self,
        dataset_id: int,
        status: ProcessingStatus,
    ) -> Optional[DatasetRegistry]:
        """
        Update processing status.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.processing_status = status

        return self.update_dataset(dataset)

    # =====================================================
    # DATA QUALITY
    # =====================================================

    def update_quality_metrics(
        self,
        dataset_id: int,
        quality_score: float,
        null_percentage: float,
        duplicate_percentage: float,
    ) -> Optional[DatasetRegistry]:
        """
        Update quality metrics.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.quality_score = quality_score
        dataset.null_percentage = null_percentage
        dataset.duplicate_percentage = duplicate_percentage

        return self.update_dataset(dataset)

    # =====================================================
    # DATASET STATISTICS
    # =====================================================

    def update_statistics(
        self,
        dataset_id: int,
        total_rows: int,
        total_columns: int,
        inserted_rows: int,
        skipped_rows: int,
        duplicate_rows: int,
    ) -> Optional[DatasetRegistry]:
        """
        Update dataset statistics.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.total_rows = total_rows
        dataset.total_columns = total_columns
        dataset.inserted_rows = inserted_rows
        dataset.skipped_rows = skipped_rows
        dataset.duplicate_rows = duplicate_rows

        return self.update_dataset(dataset)

    # =====================================================
    # SCHEMA INFORMATION
    # =====================================================

    def update_schema_information(
        self,
        dataset_id: int,
        detected_schema: dict,
        primary_keys: list,
        foreign_keys: list,
        detected_entities: list,
    ) -> Optional[DatasetRegistry]:
        """
        Save detected schema information.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.detected_schema = detected_schema
        dataset.detected_primary_keys = primary_keys
        dataset.detected_foreign_keys = foreign_keys
        dataset.detected_entities = detected_entities

        return self.update_dataset(dataset)

    # -----------------------------------------------------

    def update_column_metadata(
        self,
        dataset_id: int,
        column_names: list,
        data_types: dict,
        memory_mb: float,
    ) -> Optional[DatasetRegistry]:
        """
        Store dataset column metadata.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.column_names = column_names
        dataset.data_types = data_types
        dataset.memory_mb = memory_mb

        return self.update_dataset(dataset)

    # =====================================================
    # PROCESSING INFORMATION
    # =====================================================

    def update_processing_metadata(
        self,
        dataset_id: int,
        processing_time_seconds: float,
        uploaded_by: Optional[str] = None,
        last_processed_at=None,
    ) -> Optional[DatasetRegistry]:
        """
        Update processing metadata.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.processing_time_seconds = processing_time_seconds

        if uploaded_by is not None:
            dataset.uploaded_by = uploaded_by

        if last_processed_at is not None:
            dataset.last_processed_at = last_processed_at

        return self.update_dataset(dataset)

    # =====================================================
    # GRAPH PROCESSING
    # =====================================================

    def update_graph_statistics(
        self,
        dataset_id: int,
        graph_nodes: int,
        graph_edges: int,
    ) -> Optional[DatasetRegistry]:
        """
        Update graph statistics.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.graph_nodes = graph_nodes
        dataset.graph_edges = graph_edges

        return self.update_dataset(dataset)

    # -----------------------------------------------------

    def mark_graph_created(
        self,
        dataset_id: int,
        created: bool = True,
    ) -> Optional[DatasetRegistry]:
        """
        Mark graph creation status.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.graph_created = created

        return self.update_dataset(dataset)

    # -----------------------------------------------------

    def mark_graph_processed(
        self,
        dataset_id: int,
        processed: bool = True,
    ) -> Optional[DatasetRegistry]:
        """
        Mark graph processing completion.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.graph_processed = processed

        return self.update_dataset(dataset)

    # -----------------------------------------------------

    def mark_embeddings_generated(
        self,
        dataset_id: int,
        generated: bool = True,
    ) -> Optional[DatasetRegistry]:
        """
        Mark embedding generation.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.embeddings_generated = generated

        return self.update_dataset(dataset)

    # -----------------------------------------------------

    def mark_link_prediction_completed(
        self,
        dataset_id: int,
        completed: bool = True,
    ) -> Optional[DatasetRegistry]:
        """
        Mark link prediction completion.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.link_prediction_completed = completed

        return self.update_dataset(dataset)

    # =====================================================
    # AML PROCESSING
    # =====================================================

    def mark_entity_resolution_completed(
        self,
        dataset_id: int,
        completed: bool = True,
    ) -> Optional[DatasetRegistry]:
        """
        Mark entity resolution completion.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.entity_resolution_completed = completed

        return self.update_dataset(dataset)

    # -----------------------------------------------------

    def mark_risk_scoring_completed(
        self,
        dataset_id: int,
        completed: bool = True,
    ) -> Optional[DatasetRegistry]:
        """
        Mark risk scoring completion.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.risk_scoring_completed = completed

        return self.update_dataset(dataset)

    # -----------------------------------------------------

    def mark_investigation_ready(
        self,
        dataset_id: int,
        ready: bool = True,
    ) -> Optional[DatasetRegistry]:
        """
        Mark dataset ready for investigation.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return None

        dataset.investigation_ready = ready

        return self.update_dataset(dataset)
    
        # =====================================================
    # DASHBOARD QUERIES
    # =====================================================

    def total_datasets(self) -> int:
        """
        Total registered datasets.
        """

        return self.db.query(
            func.count(DatasetRegistry.dataset_id)
        ).scalar() or 0

    # -----------------------------------------------------

    def total_active_datasets(self) -> int:
        """
        Total active datasets.
        """

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.is_active.is_(True)
            )
            .count()
        )

    # -----------------------------------------------------

    def total_rows(self) -> int:
        """
        Sum of rows across all datasets.
        """

        return (
            self.db.query(
                func.coalesce(
                    func.sum(DatasetRegistry.total_rows),
                    0,
                )
            ).scalar()
            or 0
        )

    # -----------------------------------------------------

    def average_quality_score(self) -> float:
        """
        Average quality score.
        """

        score = self.db.query(
            func.avg(
                DatasetRegistry.quality_score
            )
        ).scalar()

        return round(score or 0, 2)

    # -----------------------------------------------------

    def successful_uploads(self) -> int:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.upload_status
                == UploadStatus.SUCCESS
            )
            .count()
        )

    # -----------------------------------------------------

    def failed_uploads(self) -> int:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.upload_status
                == UploadStatus.FAILED
            )
            .count()
        )

    # -----------------------------------------------------

    def pending_uploads(self) -> int:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.upload_status
                == UploadStatus.PENDING
            )
            .count()
        )

    # -----------------------------------------------------

    def processing_datasets(self) -> int:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.processing_status
                == ProcessingStatus.PROCESSING
            )
            .count()
        )

    # -----------------------------------------------------

    def dashboard_summary(self) -> Dict:
        """
        Dashboard summary.
        """

        return {

            "total_datasets":
                self.total_datasets(),

            "active_datasets":
                self.total_active_datasets(),

            "total_rows":
                self.total_rows(),

            "average_quality_score":
                self.average_quality_score(),

            "successful_uploads":
                self.successful_uploads(),

            "failed_uploads":
                self.failed_uploads(),

            "pending_uploads":
                self.pending_uploads(),

            "processing":
                self.processing_datasets(),

        }

    # =====================================================
    # GRAPH QUERIES
    # =====================================================

    def datasets_ready_for_graph(
        self,
    ) -> List[DatasetRegistry]:
        """
        Datasets ready for graph creation.
        """

        return (

            self.db.query(
                DatasetRegistry
            )

            .filter(
                DatasetRegistry.upload_status
                == UploadStatus.SUCCESS
            )

            .filter(
                DatasetRegistry.graph_created.is_(False)
            )

            .filter(
                DatasetRegistry.is_active.is_(True)
            )

            .all()

        )

    # -----------------------------------------------------

    def graph_created_datasets(
        self,
    ) -> List[DatasetRegistry]:

        return (

            self.db.query(
                DatasetRegistry
            )

            .filter(
                DatasetRegistry.graph_created.is_(True)
            )

            .all()

        )

    # -----------------------------------------------------

    def graph_processed_datasets(
        self,
    ) -> List[DatasetRegistry]:

        return (

            self.db.query(
                DatasetRegistry
            )

            .filter(
                DatasetRegistry.graph_processed.is_(True)
            )

            .all()

        )

    # -----------------------------------------------------

    def total_graph_nodes(self) -> int:

        return (

            self.db.query(

                func.coalesce(

                    func.sum(
                        DatasetRegistry.graph_nodes
                    ),

                    0,

                )

            ).scalar()

            or 0

        )

    # -----------------------------------------------------

    def total_graph_edges(self) -> int:

        return (

            self.db.query(

                func.coalesce(

                    func.sum(
                        DatasetRegistry.graph_edges
                    ),

                    0,

                )

            ).scalar()

            or 0

        )

    # -----------------------------------------------------

    def graph_summary(self) -> Dict:

        return {

            "datasets":

                len(
                    self.graph_created_datasets()
                ),

            "processed":

                len(
                    self.graph_processed_datasets()
                ),

            "nodes":

                self.total_graph_nodes(),

            "edges":

                self.total_graph_edges(),

        }

    # =====================================================
    # INVESTIGATION QUERIES
    # =====================================================

    def investigation_ready_datasets(
        self,
    ) -> List[DatasetRegistry]:

        return (

            self.db.query(
                DatasetRegistry
            )

            .filter(
                DatasetRegistry.investigation_ready.is_(True)
            )

            .all()

        )

    # -----------------------------------------------------

    def entity_resolution_completed(
        self,
    ) -> List[DatasetRegistry]:

        return (

            self.db.query(
                DatasetRegistry
            )

            .filter(
                DatasetRegistry.entity_resolution_completed.is_(True)
            )

            .all()

        )

    # -----------------------------------------------------

    def risk_scoring_completed(
        self,
    ) -> List[DatasetRegistry]:

        return (

            self.db.query(
                DatasetRegistry
            )

            .filter(
                DatasetRegistry.risk_scoring_completed.is_(True)
            )

            .all()

        )

    # -----------------------------------------------------

    def datasets_by_type(
        self,
    ) -> Dict[str, int]:
        """
        Dataset counts grouped by dataset_type.
        """

        rows = (

            self.db.query(

                DatasetRegistry.dataset_type,

                func.count(
                    DatasetRegistry.dataset_id
                ),

            )

            .group_by(
                DatasetRegistry.dataset_type
            )

            .all()

        )

        return {

            dataset_type or "UNKNOWN": count

            for dataset_type, count in rows

        }

    # -----------------------------------------------------

    def quality_distribution(
        self,
    ) -> Dict:
        """
        Dataset quality distribution.
        """

        return {

            "excellent":

                self.db.query(DatasetRegistry)

                .filter(
                    DatasetRegistry.quality_score >= 90
                )

                .count(),

            "good":

                self.db.query(DatasetRegistry)

                .filter(
                    DatasetRegistry.quality_score.between(
                        75,
                        89.99,
                    )
                )

                .count(),

            "poor":

                self.db.query(DatasetRegistry)

                .filter(
                    DatasetRegistry.quality_score < 75
                )

                .count(),

        }
        
        # =====================================================
    # DELETE
    # =====================================================

    def soft_delete(
        self,
        dataset_id: int,
    ) -> bool:
        """
        Soft delete dataset.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return False

        dataset.is_active = False

        self.update_dataset(dataset)

        logger.info(
            "Dataset soft deleted: %s",
            dataset.dataset_name,
        )

        return True

    # -----------------------------------------------------

    def restore(
        self,
        dataset_id: int,
    ) -> bool:
        """
        Restore a soft deleted dataset.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return False

        dataset.is_active = True

        self.update_dataset(dataset)

        return True

    # -----------------------------------------------------

    def hard_delete(
        self,
        dataset_id: int,
    ) -> bool:
        """
        Permanently delete dataset.
        """

        dataset = self.get_by_id(dataset_id)

        if dataset is None:
            return False

        self.db.delete(dataset)
        self.db.commit()

        logger.info(
            "Dataset permanently deleted: %s",
            dataset.dataset_name,
        )

        return True

    # =====================================================
    # PAGINATION
    # =====================================================

    def paginate(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict:
        """
        Paginated dataset list.
        """

        page = max(page, 1)
        page_size = max(page_size, 1)

        query = self.db.query(DatasetRegistry)

        total = query.count()

        items = (
            query.order_by(
                DatasetRegistry.created_at.desc()
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return {

            "page": page,

            "page_size": page_size,

            "total": total,

            "pages": (
                (total + page_size - 1)
                // page_size
            ),

            "items": items,

        }

    # =====================================================
    # BULK OPERATIONS
    # =====================================================

    def bulk_create(
        self,
        datasets: List[DatasetRegistry],
    ) -> int:
        """
        Bulk insert datasets.
        """

        if not datasets:
            return 0

        self.db.add_all(datasets)
        self.db.commit()

        logger.info(
            "%s datasets registered.",
            len(datasets),
        )

        return len(datasets)

    # -----------------------------------------------------

    def bulk_soft_delete(
        self,
        dataset_ids: List[int],
    ) -> int:
        """
        Soft delete multiple datasets.
        """

        updated = (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.dataset_id.in_(
                    dataset_ids
                )
            )
            .update(
                {
                    DatasetRegistry.is_active: False,
                },
                synchronize_session=False,
            )
        )

        self.db.commit()

        return updated

    # =====================================================
    # INFORMATION
    # =====================================================

    def count(self) -> int:
        """
        Total dataset count.
        """

        return (
            self.db.query(DatasetRegistry)
            .count()
        )

    # -----------------------------------------------------

    def exists(
        self,
        dataset_id: int,
    ) -> bool:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.dataset_id
                == dataset_id
            )
            .count()
            > 0
        )

    # -----------------------------------------------------

    def is_table_registered(
        self,
        table_name: str,
    ) -> bool:

        return (
            self.db.query(DatasetRegistry)
            .filter(
                DatasetRegistry.table_name
                == table_name
            )
            .count()
            > 0
        )

    # -----------------------------------------------------

    def latest_dataset(
        self,
    ) -> Optional[DatasetRegistry]:
        """
        Most recently uploaded dataset.
        """

        return (
            self.db.query(DatasetRegistry)
            .order_by(
                DatasetRegistry.created_at.desc()
            )
            .first()
        )

    # -----------------------------------------------------

    def repository_summary(self) -> Dict:
        """
        Repository summary.
        """

        return {

            "total_datasets":
                self.total_datasets(),

            "active_datasets":
                self.total_active_datasets(),

            "successful_uploads":
                self.successful_uploads(),

            "failed_uploads":
                self.failed_uploads(),

            "graph_created":
                len(
                    self.graph_created_datasets()
                ),

            "graph_processed":
                len(
                    self.graph_processed_datasets()
                ),

            "investigation_ready":
                len(
                    self.investigation_ready_datasets()
                ),

            "average_quality_score":
                self.average_quality_score(),

            "total_rows":
                self.total_rows(),

        }

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health_check(self) -> Dict:
        try:

            self.db.execute(text("SELECT 1"))

            return {
                "status": "healthy",
                "repository": self.__class__.__name__,
            }

        except Exception as ex:

            logger.exception(ex)

            return {
                "status": "unhealthy",
                "error": str(ex),
            }