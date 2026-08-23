"""
==========================================================
AML Investigation Platform

Main Application

Responsibilities
----------------
✓ Create FastAPI application
✓ Configure middleware
✓ Initialize PostgreSQL
✓ Register routers
✓ Health check endpoints
✓ Startup & Shutdown events

==========================================================
"""

import traceback
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.upload.router import router as upload_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.connection import (
    check_database_connection,
    init_db,
)

from app.api.investigation.router import (
    router as investigation_router,
)
from fastapi.openapi.utils import get_openapi
from app.api.auth.router import router as auth_router
# ==========================================================
# Application Lifecycle
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    print("\n======================================")
    print(f"Starting {settings.APP_NAME}")
    print("======================================")

    try:
        # Verify database connection
        print("Checking PostgreSQL connection...")

        db_connected = check_database_connection()

        if not db_connected:
            raise RuntimeError("check_database_connection() returned False")

        print("✓ PostgreSQL Connection Successful")

        # Create metadata tables
        print("Initializing database tables...")
        init_db()

        print("✓ Metadata Tables Initialized")
        print("✓ Application Ready")
        print("======================================\n")

    except Exception as e:
        print("\n======================================")
        print("DATABASE STARTUP ERROR")
        print("======================================")
        print(f"Exception Type : {type(e).__name__}")
        print(f"Exception      : {e}")
        print("--------------------------------------")
        traceback.print_exc()
        print("======================================\n")

        raise RuntimeError(f"Unable to connect to PostgreSQL: {e}") from e

    yield

    print("\nShutting down AML Investigation Platform...\n")


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AML Investigation Platform for Shell Company Detection using Knowledge Graphs",
    debug=settings.DEBUG,
    lifespan=lifespan,
)



# ==========================================================
# CORS Configuration
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/", tags=["Root"])
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "status": "running"
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health", tags=["Health"])
def health_check():

    database_status = (
        "healthy"
        if check_database_connection()
        else "unhealthy"
    )

    return {
        "application": settings.APP_NAME,
        "database": database_status,
        "status": "healthy"
        if database_status == "healthy"
        else "degraded"
    }
    
# ==========================================================
# API Routers
# ==========================================================

app.include_router(
    investigation_router,
    prefix="/api/v1",
)


app.include_router(
    auth_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    upload_router,
    prefix=settings.API_PREFIX,
)
