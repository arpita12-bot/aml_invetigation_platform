from pydantic import BaseModel
from typing import List


class UploadedDatasetDTO(BaseModel):
    dataset_name: str
    table_name: str
    records: int
    status: str
    message: str


class UploadResponseDTO(BaseModel):
    success: bool
    total_files: int
    uploaded_files: int
    failed_files: int
    datasets: List[UploadedDatasetDTO]