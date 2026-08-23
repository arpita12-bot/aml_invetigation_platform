"""
==========================================================
AML Investigation Platform

Upload Composition Root
==========================================================
"""

from sqlalchemy.orm import Session

from app.api.upload.controller import UploadController
from app.services.upload.services.upload_service import UploadService


class UploadContainer:

    def __init__(self, db: Session):

        self.service = UploadService(
            db=db,
        )

        self.controller = UploadController(
            self.service,
        )