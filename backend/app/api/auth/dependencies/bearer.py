from fastapi.security import HTTPBearer

JwtBearer = HTTPBearer(
    bearerFormat="JWT",
    description="Enter JWT access token",
)