from fastapi import UploadFile
from typing import List

from app.api.upload.upload_response_dto import UploadResponseDTO
from app.services.upload.services.upload_service import UploadService


class UploadController:

    def __init__(self, service: UploadService):
        self.service = service

    def upload(
        self,
        files: List[UploadFile],
    ) -> UploadResponseDTO:

        return self.service.upload(files)