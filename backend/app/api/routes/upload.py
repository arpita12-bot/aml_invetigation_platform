"""
==========================================================
AML Investigation Platform

Upload API

Responsibilities
----------------
✓ Upload datasets
✓ Validate datasets
✓ Profile datasets
✓ Dataset management
✓ Dashboard endpoints

==========================================================
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
    status,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.upload_orchestrator import (
    UploadOrchestrator,
)

from app.repositories.dataset_registry_repository import (
    DatasetRegistryRepository,
)

from app.api.auth.dependencies.authorization import (
    get_current_user,
)

from app.models.user import User


logger = logging.getLogger(__name__)


router = APIRouter(

    prefix="/upload",

    tags=["Dataset Upload"],

)

# ==========================================================
# Upload Dataset
# ==========================================================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def upload_dataset(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    ),

):
    """
    Upload dataset into AML Platform.
    """

    try:

        orchestrator = UploadOrchestrator(db)

        result = await orchestrator.upload(

            upload=file,

            uploaded_by=current_user.username,

        )

        return result

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(

            status_code=500,

            detail=str(ex),

        )
# ==========================================================
# Validate Dataset
# ==========================================================

@router.post("/validate")
async def validate_dataset(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

):

    """
    Validate uploaded dataset without loading it.
    """

    try:

        orchestrator = UploadOrchestrator(db)

        return await orchestrator.validate_only(

            file

        )

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(

            status_code=500,

            detail=str(ex),

        )
        
# ==========================================================
# Profile Dataset
# ==========================================================

@router.post("/profile")
async def profile_dataset(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

):

    """
    Generate complete dataset profile.
    """

    try:

        orchestrator = UploadOrchestrator(db)

        return await orchestrator.profile_only(

            file

        )

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(

            status_code=500,

            detail=str(ex),

        )
        
# ==========================================================
# Upload Statistics
# ==========================================================

@router.get("/statistics")
def statistics(

    db: Session = Depends(get_db),

):

    """
    Upload statistics.
    """

    orchestrator = UploadOrchestrator(db)

    return orchestrator.statistics()

# ==========================================================
# Health Check
# ==========================================================

@router.get("/health")
def health(

    db: Session = Depends(get_db),

):

    """
    Upload module health.
    """

    orchestrator = UploadOrchestrator(db)

    return orchestrator.health_check()

# ==========================================================
# List Datasets
# ==========================================================

@router.get("/datasets")
def list_datasets(

    active_only: bool = Query(
        True,
        description="Return only active datasets"
    ),

    db: Session = Depends(get_db),

):
    """
    List uploaded datasets.
    """

    repo = DatasetRegistryRepository(db)

    if active_only:
        return repo.list_active_datasets()

    return repo.list_datasets()


# ==========================================================
# Get Dataset
# ==========================================================

@router.get("/datasets/{dataset_id}")
def get_dataset(

    dataset_id: int,

    db: Session = Depends(get_db),

):
    """
    Get dataset details.
    """

    repo = DatasetRegistryRepository(db)

    dataset = repo.get_by_id(dataset_id)

    if dataset is None:

        raise HTTPException(

            status_code=404,

            detail="Dataset not found.",

        )

    return dataset


# ==========================================================
# Search Dataset
# ==========================================================

@router.get("/search")
def search_dataset(

    keyword: str,

    db: Session = Depends(get_db),

):
    """
    Search datasets.
    """

    repo = DatasetRegistryRepository(db)

    return repo.search(keyword)


# ==========================================================
# Recent Uploads
# ==========================================================

@router.get("/recent")
def recent_uploads(

    limit: int = Query(
        10,
        ge=1,
        le=100,
    ),

    db: Session = Depends(get_db),

):
    """
    Recent uploads.
    """

    repo = DatasetRegistryRepository(db)

    return repo.recent_uploads(limit)


# ==========================================================
# Pagination
# ==========================================================

@router.get("/paginate")
def paginate(

    page: int = Query(
        1,
        ge=1,
    ),

    page_size: int = Query(
        20,
        ge=1,
        le=100,
    ),

    db: Session = Depends(get_db),

):
    """
    Paginated datasets.
    """

    repo = DatasetRegistryRepository(db)

    return repo.paginate(

        page=page,

        page_size=page_size,

    )
    
# ==========================================================
# Dashboard Summary
# ==========================================================

@router.get("/dashboard")
def dashboard(

    db: Session = Depends(get_db),

):
    """
    Dashboard summary.
    """

    repo = DatasetRegistryRepository(db)

    return repo.dashboard_summary()


# ==========================================================
# Repository Summary
# ==========================================================

@router.get("/summary")
def repository_summary(

    db: Session = Depends(get_db),

):
    """
    Repository summary.
    """

    repo = DatasetRegistryRepository(db)

    return repo.repository_summary()


# ==========================================================
# Dataset Types
# ==========================================================

@router.get("/types")
def dataset_types(

    db: Session = Depends(get_db),

):
    """
    Dataset counts by type.
    """

    repo = DatasetRegistryRepository(db)

    return repo.datasets_by_type()


# ==========================================================
# Quality Distribution
# ==========================================================

@router.get("/quality")
def quality_distribution(

    db: Session = Depends(get_db),

):
    """
    Quality distribution.
    """

    repo = DatasetRegistryRepository(db)

    return repo.quality_distribution()

# ==========================================================
# Graph Summary
# ==========================================================

@router.get("/graph")
def graph_summary(

    db: Session = Depends(get_db),

):
    """
    Graph summary.
    """

    repo = DatasetRegistryRepository(db)

    return repo.graph_summary()


# ==========================================================
# Graph Ready Datasets
# ==========================================================

@router.get("/graph/ready")
def graph_ready(

    db: Session = Depends(get_db),

):
    """
    Datasets waiting for graph creation.
    """

    repo = DatasetRegistryRepository(db)

    return repo.datasets_ready_for_graph()


# ==========================================================
# Graph Processed
# ==========================================================

@router.get("/graph/processed")
def graph_processed(

    db: Session = Depends(get_db),

):
    """
    Graph processed datasets.
    """

    repo = DatasetRegistryRepository(db)

    return repo.graph_processed_datasets()

# ==========================================================
# Investigation Ready
# ==========================================================

@router.get("/investigation")
def investigation_ready(

    db: Session = Depends(get_db),

):
    """
    Investigation ready datasets.
    """

    repo = DatasetRegistryRepository(db)

    return repo.investigation_ready_datasets()


# ==========================================================
# Entity Resolution
# ==========================================================

@router.get("/entity-resolution")
def entity_resolution(

    db: Session = Depends(get_db),

):
    """
    Entity resolution completed datasets.
    """

    repo = DatasetRegistryRepository(db)

    return repo.entity_resolution_completed()


# ==========================================================
# Risk Scoring
# ==========================================================

@router.get("/risk-scoring")
def risk_scoring(

    db: Session = Depends(get_db),

):
    """
    Risk scoring completed datasets.
    """

    repo = DatasetRegistryRepository(db)

    return repo.risk_scoring_completed()

# ==========================================================
# Soft Delete Dataset
# ==========================================================

@router.delete("/datasets/{dataset_id}")
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Soft delete dataset.
    """

    repo = DatasetRegistryRepository(db)

    deleted = repo.soft_delete(dataset_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )

    return {
        "success": True,
        "message": "Dataset deleted successfully."
    }


# ==========================================================
# Restore Dataset
# ==========================================================

@router.post("/datasets/{dataset_id}/restore")
def restore_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Restore a previously deleted dataset.
    """

    repo = DatasetRegistryRepository(db)

    restored = repo.restore(dataset_id)

    if not restored:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )

    return {
        "success": True,
        "message": "Dataset restored successfully."
    }


# ==========================================================
# Hard Delete Dataset
# ==========================================================

@router.delete("/datasets/{dataset_id}/hard")
def hard_delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Permanently delete dataset.
    """

    repo = DatasetRegistryRepository(db)

    deleted = repo.hard_delete(dataset_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )

    return {
        "success": True,
        "message": "Dataset permanently deleted."
    }


# ==========================================================
# Retry Upload
# ==========================================================

@router.post("/retry/{dataset_id}")
def retry_upload(
    dataset_id: int,
    db: Session = Depends(get_db),
):
    """
    Retry failed upload.
    """

    orchestrator = UploadOrchestrator(db)

    return orchestrator.retry_upload(dataset_id)


# ==========================================================
# Upload Summary
# ==========================================================

@router.get("/summary/upload")
def upload_summary(
    db: Session = Depends(get_db),
):
    """
    Upload summary.
    """

    orchestrator = UploadOrchestrator(db)

    return orchestrator.build_upload_summary()


# ==========================================================
# Module Information
# ==========================================================

@router.get("/info")
def module_info(
    db: Session = Depends(get_db),
):
    """
    Upload module information.
    """

    orchestrator = UploadOrchestrator(db)

    return orchestrator.info()


# ==========================================================
# Repository Health
# ==========================================================

@router.get("/repository/health")
def repository_health(
    db: Session = Depends(get_db),
):
    """
    Dataset repository health.
    """

    repo = DatasetRegistryRepository(db)

    return repo.health_check()


# ==========================================================
# Dataset Exists
# ==========================================================

@router.get("/exists/{dataset_name}")
def dataset_exists(
    dataset_name: str,
    db: Session = Depends(get_db),
):
    """
    Check whether dataset exists.
    """

    repo = DatasetRegistryRepository(db)

    return {
        "exists": repo.dataset_exists(dataset_name)
    }


# ==========================================================
# Total Dataset Count
# ==========================================================

@router.get("/count")
def dataset_count(
    db: Session = Depends(get_db),
):
    """
    Total datasets.
    """

    repo = DatasetRegistryRepository(db)

    return {
        "count": repo.count()
    }


# ==========================================================
# Latest Dataset
# ==========================================================

@router.get("/latest")
def latest_dataset(
    db: Session = Depends(get_db),
):
    """
    Latest uploaded dataset.
    """

    repo = DatasetRegistryRepository(db)

    return repo.latest_dataset()