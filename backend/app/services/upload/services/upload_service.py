from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import List

import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.api.upload.upload_response_dto import (
    UploadResponseDTO,
    UploadedDatasetDTO,
)
from app.services.schema.schema_inference import SchemaInferenceService
from app.services.ingestion.dataset_ingestion_service import (
    DatasetIngestionService,
)


class UploadService:

    def __init__(self, db: Session):
        self.db = db

    def upload(
        self,
        files: List[UploadFile],
    ) -> UploadResponseDTO:

        uploaded_files = []
        failed_files = []
        datasets = []

        for file in files:

            temp_path = None

            try:

                # ----------------------------------
                # Save temporary file
                # ----------------------------------

                suffix = Path(file.filename).suffix

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                ) as tmp:

                    tmp.write(file.file.read())
                    temp_path = tmp.name

                # ----------------------------------
                # Read dataframe
                # ----------------------------------

                df = pd.read_csv(temp_path)

                file_size_mb = round(
                    os.path.getsize(temp_path) / (1024 * 1024),
                    2,
                )

                dataset_name = Path(file.filename).stem

                table_name = (
                    dataset_name.lower()
                    .replace(" ", "_")
                    .replace("-", "_")
                )

                # ----------------------------------
                # Schema Inference
                # ----------------------------------

                schema_result = SchemaInferenceService.infer(
                    dataframe=df,
                    dataset_name=dataset_name,
                    original_filename=file.filename,
                    table_name=table_name,
                    dataset_type="AML",
                    file_size_mb=file_size_mb,
                )

                if not schema_result.successful:

                    failed_files.append(file.filename)

                    datasets.append(
                        UploadedDatasetDTO(
                            dataset_name=dataset_name,
                            table_name=table_name,
                            records=0,
                            status="FAILED",
                            message="Schema inference failed.",
                        )
                    )

                    continue

                # ----------------------------------
                # Dataset Ingestion
                # ----------------------------------

                result = DatasetIngestionService.ingest(
                    session=self.db,
                    dataframe=df,
                    metadata=schema_result.metadata,
                    generate_graph=True,
                )

                if result.successful:

                    uploaded_files.append(file.filename)

                    datasets.append(
                        UploadedDatasetDTO(
                            dataset_name=dataset_name,
                            table_name=table_name,
                            records=len(df),
                            status="SUCCESS",
                            message="Dataset uploaded successfully.",
                        )
                    )

                else:

                    failed_files.append(file.filename)

                    error_message = (
                        "; ".join(result.errors)
                        if result.errors
                        else (
                            result.failed_statement
                            if result.failed_statement
                            else "Dataset ingestion failed."
                        )
                    )

                    datasets.append(
                        UploadedDatasetDTO(
                            dataset_name=dataset_name,
                            table_name=table_name,
                            records=len(df),
                            status="FAILED",
                            message=error_message,
                        )
                    )

            except Exception as ex:

                print(ex)

                failed_files.append(file.filename)

                datasets.append(
                    UploadedDatasetDTO(
                        dataset_name=Path(file.filename).stem,
                        table_name="",
                        records=0,
                        status="FAILED",
                        message=str(ex),
                    )
                )

            finally:

                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

        return UploadResponseDTO(
            success=len(failed_files) == 0,
            total_files=len(files),
            uploaded_files=len(uploaded_files),
            failed_files=len(failed_files),
            datasets=datasets,
        )