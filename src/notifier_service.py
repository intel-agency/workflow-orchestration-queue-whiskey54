"""Notifier Service - FastAPI application for handling notifications.

This service provides HTTP endpoints for:
- Health checks
- Webhook receipt from GitHub events
- Notification queue management
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Notifier Service",
    description="FastAPI service for handling workflow notifications",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint for container orchestration."""
    return HealthResponse(status="healthy", version="0.1.0")


@app.get("/ready", response_model=HealthResponse)
async def readiness_check() -> HealthResponse:
    """Readiness check endpoint for container orchestration."""
    # TODO: Add dependency checks (database, queue, etc.)
    return HealthResponse(status="ready", version="0.1.0")


def main() -> None:
    """Entry point for the notifier service."""
    import uvicorn

    uvicorn.run(
        "src.notifier_service:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
