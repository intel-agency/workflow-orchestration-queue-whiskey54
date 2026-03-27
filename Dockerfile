# Dockerfile for Workflow Orchestration Queue Service
# Multi-stage build for optimized production image

# =============================================================================
# Build stage - install dependencies
# =============================================================================
FROM python:3.12-slim AS builder

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml ./

# Install dependencies to a virtual environment
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --no-cache -e .

# =============================================================================
# Production stage
# =============================================================================
FROM python:3.12-slim AS production

# Create non-root user for security
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appgroup src/ ./src/
COPY --chown=appuser:appgroup pyproject.toml ./

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Health check using Python stdlib (no curl required)
# Uses urllib to check the health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Default command runs the notifier service
CMD ["python", "-m", "src.notifier_service"]
