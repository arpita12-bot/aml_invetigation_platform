"""
Authentication Schemas
"""

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):

    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class LoginRequest(BaseModel):

    username: str
    password: str


class UserResponse(BaseModel):

    id: int
    username: str
    email: str
    role: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"
    user: UserResponse