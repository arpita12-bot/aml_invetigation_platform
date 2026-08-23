"""
==========================================================
AML Investigation Platform

Enterprise Dataset Profiler

Responsibilities
----------------
✓ Dataset statistics
✓ Column profiling
✓ Candidate key detection
✓ Data quality metrics
✓ PII detection
✓ AML identifier detection
✓ Numeric statistics
✓ Dashboard metadata
✓ Entity Resolution support

==========================================================
"""

from __future__ import annotations

import logging
import re

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class DatasetProfiler:
    """
    Enterprise Dataset Profiler.

    Generates dataset metadata used by:

    - Dashboard
    - Upload Summary
    - Entity Resolution
    - AI Copilot
    - Investigation Engine
    """

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    PHONE_PATTERN = re.compile(
        r"^[0-9+\-\s()]{7,20}$"
    )

    SAMPLE_SIZE = 100

    def __init__(self):
        logger.info("DatasetProfiler initialized.")
        
    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _validate_dataframe(
        self,
        df: Optional[pd.DataFrame],
    ) -> None:
        """
        Validate dataframe input.
        """

        if df is None:
            raise ValueError("DataFrame cannot be None.")

    def _sample(
        self,
        series: pd.Series,
    ) -> pd.Series:
        """
        Return a representative sample
        from a dataframe column.
        """

        return (
            series
            .dropna()
            .astype(str)
            .head(self.SAMPLE_SIZE)
        )

    def _safe_round(
        self,
        value: Any,
        digits: int = 2,
    ):
        """
        Safely round numeric values.
        """

        try:
            return round(float(value), digits)

        except Exception:
            return None
    # ---------------------------------------------------------
    # Dataset Summary
    # ---------------------------------------------------------

    def summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Overall dataset statistics.
        """

        self._validate_dataframe(df)

        logger.info("Generating dataset summary.")

        return {

            "rows": len(df),

            "columns": len(df.columns),

            "memory_mb": self._safe_round(

                df.memory_usage(
                    deep=True
                ).sum() / 1024 / 1024

            ),

            "duplicate_rows": int(

                df.duplicated().sum()

            ),

            "duplicate_percent": self._safe_round(

                df.duplicated().mean() * 100

            ),

        }
        
    # ---------------------------------------------------------
    # Null Summary
    # ---------------------------------------------------------

    def null_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate null statistics.
        """

        self._validate_dataframe(df)

        logger.info("Calculating null summary.")

        results = {}

        total_rows = len(df)

        for column in df.columns:

            nulls = int(
                df[column].isna().sum()
            )

            results[column] = {

                "null_count": nulls,

                "null_percent": self._safe_round(

                    (
                        nulls / total_rows * 100
                    )

                    if total_rows

                    else 0

                ),

            }

        return results
    
    # ---------------------------------------------------------
    # Unique Values
    # ---------------------------------------------------------

    def unique_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Analyze unique values.
        """

        self._validate_dataframe(df)

        logger.info("Calculating unique statistics.")

        results = {}

        total_rows = len(df)

        for column in df.columns:

            unique_count = int(

                df[column].nunique(
                    dropna=True
                )

            )

            results[column] = {

                "unique_count": unique_count,

                "duplicate_count": max(
                    0,
                    total_rows - unique_count,
                ),

                "is_unique": bool(
                    df[column].is_unique
                ),

            }

        return results
    
    # ---------------------------------------------------------
    # Candidate Keys
    # ---------------------------------------------------------

    def candidate_keys(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Identify columns that
        can act as primary keys.
        """

        self._validate_dataframe(df)

        logger.info(
            "Finding candidate keys."
        )

        keys = []

        for column in df.columns:

            if (

                df[column].notna().all()

                and

                df[column].is_unique

            ):

                keys.append(column)

        return keys
    
    # ---------------------------------------------------------
    # Column Types
    # ---------------------------------------------------------

    def column_types(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, str]:
        """
        Return pandas dtypes.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting column types."
        )

        return {

            column: str(
                df[column].dtype
            )

            for column in df.columns

        }
        
    # ---------------------------------------------------------
    # Email Detection
    # ---------------------------------------------------------

    def detect_email_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Detect email columns.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting email columns."
        )

        columns = []

        for column in df.columns:

            sample = self._sample(
                df[column]
            )

            if sample.empty:
                continue

            matches = sum(
                bool(
                    self.EMAIL_PATTERN.match(
                        value
                    )
                )
                for value in sample
            )

            if matches >= max(
                1,
                int(len(sample) * 0.8),
            ):
                columns.append(column)

        return columns
    
    # ---------------------------------------------------------
    # Phone Detection
    # ---------------------------------------------------------

    def detect_phone_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Detect phone number columns.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting phone columns."
        )

        columns = []

        for column in df.columns:

            sample = self._sample(
                df[column]
            )

            if sample.empty:
                continue

            matches = sum(
                bool(
                    self.PHONE_PATTERN.match(
                        value
                    )
                )
                for value in sample
            )

            if matches >= max(
                1,
                int(len(sample) * 0.8),
            ):
                columns.append(column)

        return columns
    
    # ---------------------------------------------------------
    # AML Identifier Detection
    # ---------------------------------------------------------

    def identifier_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Detect AML identifier columns.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting identifier columns."
        )

        keywords = {

            "id",

            "customer",

            "customer_id",

            "client",

            "client_id",

            "account",

            "account_id",

            "transaction",

            "txn",

            "employee",

            "vendor",

            "merchant",

            "beneficiary",

            "company",

            "passport",

            "pan",

            "aadhaar",

            "tax",

            "tin",

            "ifsc",

            "swift",

            "bic",

            "iban",

            "wallet",

            "email",

            "phone",

        }

        identifiers = []

        for column in df.columns:

            name = column.lower()

            if any(
                keyword in name
                for keyword in keywords
            ):
                identifiers.append(column)

        return identifiers
    
    # ---------------------------------------------------------
    # Date Detection
    # ---------------------------------------------------------

    def detect_date_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Detect date columns.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting date columns."
        )

        dates = []

        for column in df.columns:

            if pd.api.types.is_datetime64_any_dtype(
                df[column]
            ):

                dates.append(column)

                continue

            sample = (
                df[column]
                .dropna()
                .head(self.SAMPLE_SIZE)
            )

            if sample.empty:
                continue

            try:

                converted = pd.to_datetime(
                    sample,
                    errors="coerce",
                )

                if converted.notna().mean() >= 0.8:

                    dates.append(column)

            except Exception:

                continue

        return dates
    
    # ---------------------------------------------------------
    # Numeric Statistics
    # ---------------------------------------------------------

    def numeric_statistics(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Numeric statistics.
        """

        self._validate_dataframe(df)

        logger.info(
            "Calculating numeric statistics."
        )

        statistics = {}

        numeric = df.select_dtypes(
            include="number"
        )

        for column in numeric.columns:

            series = numeric[column]

            statistics[column] = {

                "count": int(
                    series.count()
                ),

                "min": self._safe_round(
                    series.min()
                ),

                "max": self._safe_round(
                    series.max()
                ),

                "mean": self._safe_round(
                    series.mean()
                ),

                "median": self._safe_round(
                    series.median()
                ),

                "std": self._safe_round(
                    series.std()
                ),

                "sum": self._safe_round(
                    series.sum()
                ),

            }

        return statistics
    
    # ---------------------------------------------------------
    # Column Classification
    # ---------------------------------------------------------

    def classify_columns(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, str]:
        """
        Classify each column by purpose.
        """

        self._validate_dataframe(df)

        logger.info(
            "Classifying columns."
        )

        emails = set(
            self.detect_email_columns(df)
        )

        phones = set(
            self.detect_phone_columns(df)
        )

        dates = set(
            self.detect_date_columns(df)
        )

        identifiers = set(
            self.identifier_columns(df)
        )

        classification = {}

        for column in df.columns:

            if column in identifiers:

                classification[column] = "IDENTIFIER"

            elif column in emails:

                classification[column] = "EMAIL"

            elif column in phones:

                classification[column] = "PHONE"

            elif column in dates:

                classification[column] = "DATE"

            elif pd.api.types.is_numeric_dtype(
                df[column]
            ):

                classification[column] = "NUMERIC"

            else:

                classification[column] = "TEXT"

        return classification
    
        # ---------------------------------------------------------
    # Dataset Metrics
    # ---------------------------------------------------------

    def dataset_metrics(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Overall dataset metrics.
        """

        self._validate_dataframe(df)

        logger.info(
            "Calculating dataset metrics."
        )

        return {

            "total_cells": int(df.size),

            "total_nulls": int(
                df.isna().sum().sum()
            ),

            "duplicate_rows": int(
                df.duplicated().sum()
            ),

            "duplicate_percent": self._safe_round(
                df.duplicated().mean() * 100
            ),

            "memory_mb": self._safe_round(
                df.memory_usage(
                    deep=True
                ).sum()
                / 1024
                / 1024
            ),

        }
        
        # ---------------------------------------------------------
    # Data Quality Score
    # ---------------------------------------------------------

    def quality_score(
        self,
        df: pd.DataFrame,
    ) -> float:
        """
        Calculate an overall quality score.
        """

        self._validate_dataframe(df)

        logger.info(
            "Calculating quality score."
        )

        if df.empty:
            return 0.0

        total_cells = df.size

        if total_cells == 0:
            return 0.0

        null_ratio = (

            df.isna()
            .sum()
            .sum()

            / total_cells

        )

        duplicate_ratio = (

            df.duplicated()
            .mean()

        )

        score = (

            100

            - (null_ratio * 50)

            - (duplicate_ratio * 50)

        )

        return round(
            max(score, 0),
            2,
        )
        
        # ---------------------------------------------------------
    # Complete Profile
    # ---------------------------------------------------------

    def profile(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Generate a complete dataset profile.
        """

        self._validate_dataframe(df)

        logger.info(
            "Generating complete dataset profile."
        )

        try:

            profile = {

                "summary":
                    self.summary(df),

                "metrics":
                    self.dataset_metrics(df),

                "null_summary":
                    self.null_summary(df),

                "unique_summary":
                    self.unique_summary(df),

                "candidate_keys":
                    self.candidate_keys(df),

                "column_types":
                    self.column_types(df),

                "column_classification":
                    self.classify_columns(df),

                "email_columns":
                    self.detect_email_columns(df),

                "phone_columns":
                    self.detect_phone_columns(df),

                "identifier_columns":
                    self.identifier_columns(df),

                "date_columns":
                    self.detect_date_columns(df),

                "numeric_statistics":
                    self.numeric_statistics(df),

                "quality_score":
                    self.quality_score(df),

            }

            logger.info(
                "Dataset profiling completed successfully."
            )

            return profile

        except Exception as ex:

            logger.exception(
                "Dataset profiling failed."
            )

            raise RuntimeError(
                f"Dataset profiling failed: {str(ex)}"
            ) from ex
    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    def health_check(self) -> Dict[str, str]:
        """
        Health status.
        """

        return {

            "service": "DatasetProfiler",

            "status": "healthy",

        }
        
    # =====================================================
    # FILE HELPERS
    # =====================================================

    def _save_upload(
        self,
        upload: UploadFile,
    ) -> Path:
        """
        Save uploaded file to a temporary location.
        """

        suffix = Path(upload.filename).suffix

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        )

        with temp_file as fp:
            shutil.copyfileobj(upload.file, fp)

        logger.info(
            "Temporary upload saved: %s",
            temp_file.name,
        )

        return Path(temp_file.name)
    
    def _file_hash(
        self,
        path: Path,
    ) -> str:
        """
        SHA256 hash.
        """

        sha = hashlib.sha256()

        with open(path, "rb") as f:

            while True:

                chunk = f.read(8192)

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()
    
    def _cleanup(
        self,
        path: Optional[Path],
    ) -> None:
        """
        Remove temporary upload.
        """

        if path is None:
            return

        try:

            if path.exists():
                path.unlink()

        except Exception:

            logger.exception(
                "Unable to delete temp file."
                )
            
    # =====================================================
    # DATASET REGISTRATION
    # =====================================================

    def _build_dataset_registry(
        self,
        metadata: Dict[str, Any],
        profile: Dict[str, Any],
        validation: Dict[str, Any],
        quality: Dict[str, Any],
        table_name: str,
        upload_path: str,
        file_hash: str,
    ) -> DatasetRegistry:
        """
        Create DatasetRegistry model.
        """

        summary = profile["summary"]

        dataset = DatasetRegistry(

            original_filename=metadata["filename"],

            sanitized_filename=metadata["filename"],

            dataset_name=metadata["dataset_name"],

            dataset_type=metadata["dataset_type"],

            file_extension=metadata["extension"],

            file_size_bytes=metadata["size"],

            mime_type=metadata["mime_type"],

            upload_path=upload_path,

            file_hash=file_hash,

            table_name=table_name,

            schema_name="public",

            total_rows=summary["rows"],

            total_columns=summary["columns"],

            inserted_rows=summary["rows"],

            skipped_rows=0,

            duplicate_rows=summary["duplicate_rows"],

            memory_mb=summary["memory_mb"],

            quality_score=profile["quality_score"],

            null_percentage=quality.get(
                "null_percentage",
                0,
            ),

            duplicate_percentage=summary[
                "duplicate_percent"
            ],

            detected_schema=validation,

            detected_primary_keys=profile[
                "candidate_keys"
            ],

            detected_foreign_keys=[],

            detected_entities=profile[
                "identifier_columns"
            ],

            column_names=list(
                profile["column_types"].keys()
            ),

            data_types=profile[
                "column_types"
            ],

            upload_status=UploadStatus.SUCCESS,

            validation_status=ValidationStatus.SUCCESS,

            processing_status=ProcessingStatus.COMPLETED,

            graph_created=False,

            graph_processed=False,

            embeddings_generated=False,

            link_prediction_completed=False,

            entity_resolution_completed=False,

            risk_scoring_completed=False,

            investigation_ready=False,

            is_active=True,

            created_at=datetime.utcnow(),

            updated_at=datetime.utcnow(),

        )

        return dataset
    
    # =====================================================
    # RESPONSE BUILDERS
    # =====================================================

    def _success_response(
        self,
        dataset: DatasetRegistry,
        profile: Dict[str, Any],
        validation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {

            "status": "SUCCESS",

            "dataset_id": dataset.dataset_id,

            "dataset_name": dataset.dataset_name,

            "table_name": dataset.table_name,

            "rows": dataset.total_rows,

            "columns": dataset.total_columns,

            "quality_score": dataset.quality_score,

            "validation": validation,

            "profile": profile,

        }
        
    
    def _failure_response(
        self,
        message: str,
    ) -> Dict[str, Any]:

        return {

            "status": "FAILED",

            "message": message,

        }
    
    
    # =====================================================
    # MAIN UPLOAD PIPELINE
    # =====================================================

    async def upload(
        self,
        upload: UploadFile,
        uploaded_by: str | None = None,
        ) -> Dict[str, Any]:
        """
        Enterprise upload workflow.

        Pipeline

        Upload
            ↓
        Loader
            ↓
        Validation
            ↓
        Quality
            ↓
        PostgreSQL
            ↓
        Profiling
            ↓
        Dataset Registry
            ↓
        Response
        """

        start = time.perf_counter()

        temp_path: Optional[Path] = None

        try:

            # -------------------------------------------------
            # Save upload temporarily
            # -------------------------------------------------

            temp_path = self._save_upload(upload)

            file_hash = self._file_hash(temp_path)

            # -------------------------------------------------
            # Prevent duplicate uploads
            # -------------------------------------------------

            if self.repository.file_already_uploaded(file_hash):

                return self._failure_response(
                    "This file has already been uploaded."
                )

            # -------------------------------------------------
            # Load dataframe
            # -------------------------------------------------

            dataframe = self.loader.load(
                str(temp_path)
            )

            logger.info(
                "Dataset loaded successfully."
            )

            # -------------------------------------------------
            # Infer metadata
            # -------------------------------------------------

            metadata = self.loader.infer_metadata(
                dataframe,
                filename=upload.filename,
            )

            table_name = metadata["dataset_name"]

            # -------------------------------------------------
            # Schema validation
            # -------------------------------------------------

            validation = self.validator.validate(
                dataframe,
                table_name,
            )

            logger.info(
                "Schema validation completed."
            )

            # -------------------------------------------------
            # Data quality
            # -------------------------------------------------

            quality = self.quality.analyze(
                dataframe
            )

            logger.info(
                "Quality analysis completed."
            )

            # -------------------------------------------------
            # Create PostgreSQL table
            # -------------------------------------------------

            self.table_creator.create_or_evolve(
                table_name,
                dataframe,
            )

            logger.info(
                "PostgreSQL table ready."
            )

            # -------------------------------------------------
            # Load records
            # -------------------------------------------------

            load_result = (
                self.postgres_loader.load_dataframe(
                    dataframe,
                    table_name,
                )
            )

            logger.info(
                "Rows inserted into PostgreSQL."
            )

            # -------------------------------------------------
            # Dataset profile
            # -------------------------------------------------

            profile = self.profiler.profile(
                dataframe
            )

            logger.info(
                "Dataset profiling completed."
            )

            # -------------------------------------------------
            # Register dataset
            # -------------------------------------------------

            dataset = self._build_dataset_registry(

                metadata=metadata,

                profile=profile,

                validation=validation,

                quality=quality,

                table_name=table_name,

                upload_path=str(temp_path),

                file_hash=file_hash,

            )

            dataset.processing_time_seconds = round(

                time.perf_counter() - start,

                2,

            )

            dataset.last_processed_at = datetime.utcnow()

            dataset.uploaded_by = uploaded_by

            dataset.inserted_rows = load_result.get(
                "inserted_rows",
                dataset.total_rows,
            )

            dataset.skipped_rows = load_result.get(
                "skipped_rows",
                0,
            )

            dataset = self.repository.create_dataset(
                dataset
            )

            logger.info(
                "Dataset registered successfully."
            )

            # -------------------------------------------------
            # Return success
            # -------------------------------------------------

            return self._success_response(

                dataset,

                profile,

                validation,

            )

        except Exception as ex:

            logger.exception(ex)

            self.db.rollback()

            return self._failure_response(
                str(ex)
            )

        finally:

            self._cleanup(temp_path)
            
    # =====================================================
    # VALIDATION ONLY
    # =====================================================

    async def validate_only(
        self,
        upload: UploadFile,
    ) -> Dict[str, Any]:

        temp_path = None

        try:

            temp_path = self._save_upload(upload)

            dataframe = self.loader.load(
                str(temp_path)
            )

            metadata = self.loader.infer_metadata(
                dataframe,
                filename=upload.filename,
            )

            validation = self.validator.validate(
                dataframe,
                metadata["dataset_name"],
            )

            quality = self.quality.analyze(
                dataframe
            )

            profile = self.profiler.profile(
                dataframe
            )

            return {

                "status": "SUCCESS",

                "metadata": metadata,

                "validation": validation,

                "quality": quality,

                "profile": profile,

            }

        finally:

            self._cleanup(temp_path)
            
    # =====================================================
    # PROFILE ONLY
    # =====================================================

    async def profile_only(
        self,
        upload: UploadFile,
    ) -> Dict[str, Any]:

        temp_path = None

        try:

            temp_path = self._save_upload(upload)

            dataframe = self.loader.load(
                str(temp_path)
            )

            return self.profiler.profile(
                dataframe
            )

        finally:

            self._cleanup(temp_path)
            
    # =====================================================
    # ROLLBACK
    # =====================================================

    def _rollback(
        self,
        ex: Exception,
    ) -> None:
        """
        Rollback database transaction.
        """

        try:

            self.db.rollback()

            logger.exception(
                "Upload failed. Transaction rolled back."
            )

            logger.exception(ex)

        except Exception as rollback_ex:

            logger.exception(
                rollback_ex
            )
            
    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self) -> Dict[str, Any]:
        """
        Upload statistics.
        """

        return {

            "datasets":

                self.repository.total_datasets(),

            "successful":

                self.repository.successful_uploads(),

            "failed":

                self.repository.failed_uploads(),

            "processing":

                self.repository.processing_datasets(),

            "average_quality":

                self.repository.average_quality_score(),

            "rows":

                self.repository.total_rows(),

        }
        
    # =====================================================
    # RETRY
    # =====================================================

    async def retry_upload(
        self,
        upload: UploadFile,
        uploaded_by: str | None = None,
    ) -> Dict[str, Any]:
        """
        Retry upload after failure.
        """

        logger.info(
            "Retry upload requested."
        )

        return await self.upload(
            upload,
            uploaded_by,
        )
        
    # =====================================================
    # AUDIT
    # =====================================================

    def audit_log(
        self,
        dataset: DatasetRegistry,
    ) -> Dict[str, Any]:
        """
        Audit metadata.
        """

        return {

            "dataset_id":

                dataset.dataset_id,

            "dataset_name":

                dataset.dataset_name,

            "uploaded_at":

                dataset.created_at,

            "uploaded_by":

                dataset.uploaded_by,

            "status":

                dataset.upload_status,

            "table":

                dataset.table_name,

        }
        
    # =====================================================
    # RESPONSE
    # =====================================================

    def build_upload_summary(
        self,
        dataset: DatasetRegistry,
        profile: Dict[str, Any],
        validation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {

            "status":

                "SUCCESS",

            "dataset": {

                "id":
                    dataset.dataset_id,

                "name":
                    dataset.dataset_name,

                "table":
                    dataset.table_name,

                "rows":
                    dataset.total_rows,

                "columns":
                    dataset.total_columns,

                "quality_score":
                    dataset.quality_score,

            },

            "validation":

                validation,

            "profile":

                profile,

            "audit":

                self.audit_log(
                    dataset
                ),

        }
        
    # =====================================================
    # HEALTH
    # =====================================================

    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Service health.
        """

        try:

            repository = self.repository.health_check()

            return {

                "service":

                    "UploadOrchestrator",

                "status":

                    "healthy",

                "repository":

                    repository,

            }

        except Exception as ex:

            logger.exception(ex)

            return {

                "service":

                    "UploadOrchestrator",

                "status":

                    "unhealthy",

                "error":

                    str(ex),

            }
            
    # =====================================================
    # INFO
    # =====================================================

    def info(
        self,
    ) -> Dict[str, Any]:
        """
        Service information.
        """

        return {

            "service":

                "UploadOrchestrator",

            "version":

                "1.0.0",

            "pipeline": [

                "DatasetLoader",

                "SchemaValidator",

                "DataQualityService",

                "DynamicTableCreator",

                "PostgresLoader",

                "DatasetProfiler",

                "DatasetRegistryRepository",

            ],

        }