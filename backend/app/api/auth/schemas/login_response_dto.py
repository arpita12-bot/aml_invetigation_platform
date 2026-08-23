from pydantic import BaseModel


class UserResponseDTO(BaseModel):

    id: int

    username: str

    email: str

    role: str


class LoginResponseDTO(BaseModel):

    access_token: str

    token_type: str = "bearer"

    user: UserResponseDTO