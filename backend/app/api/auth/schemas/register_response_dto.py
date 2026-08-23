from pydantic import BaseModel


class RegisterResponseDTO(BaseModel):

    success: bool

    message: str