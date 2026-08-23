from pydantic import BaseModel, EmailStr


class RegisterRequestDTO(BaseModel):

    username: str

    email: EmailStr

    password: str

    first_name: str

    last_name: str