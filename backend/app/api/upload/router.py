from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.api.auth.dependencies.current_user import get_current_user

from app.api.upload.upload_response_dto import UploadResponseDTO
from app.services.upload.composition.upload_container import UploadContainer

router = APIRouter(
    prefix="/upload",
    tags=["Dataset Upload"],
)


@router.post(
    "",
    response_model=UploadResponseDTO,
    summary="Upload AML datasets",
)
def upload_datasets(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> UploadResponseDTO:

    container = UploadContainer(db)

    return container.controller.upload(files)