from fastapi import APIRouter
from fastapi import Depends

from app.api.auth.dependencies.current_user import (
    get_current_user,
)

from app.api.investigation.schemas.investigation_request_dto import (
    InvestigationRequestDTO,
)

from app.api.investigation.schemas.investigation_response_dto import (
    InvestigationResponseDTO,
)

from app.api.investigation.controller import (
    InvestigationController,
)

from app.services.investigation.composition import (
    InvestigationContainer,
)

router = APIRouter(
    prefix="/investigations",
    tags=["AML Investigation"],
)


def get_controller() -> InvestigationController:
    return InvestigationContainer.build_controller()


@router.post(
    "",
    response_model=InvestigationResponseDTO,
    summary="Execute AML Investigation",
)
def investigate(
    request: InvestigationRequestDTO,
    current_user=Depends(get_current_user),
) -> InvestigationResponseDTO:

    return get_controller().investigate(request)