# Workflow Orchestration Queue Service

A FastAPI-based service for handling GitHub webhook events and managing a workflow orchestration queue.

## Overview

This service provides:

- **Notifier Service**: FastAPI application for receiving GitHub webhooks and managing notifications
- **Orchestrator Sentinel**: Background service for monitoring orchestration state and processing work items
- **GitHub Queue**: In-memory queue for managing work items with priority support and retry logic

## Tech Stack

- **Python**: 3.12+
- **FastAPI**: Modern async web framework
- **Pydantic**: Data validation and settings management
- **HTTPX**: Async HTTP client
- **uv**: Fast Python package manager

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── notifier_service.py      # FastAPI application
│   ├── orchestrator_sentinel.py # Background monitoring service
│   ├── models/
│   │   ├── __init__.py
│   │   ├── work_item.py         # Work item data models
│   │   └── github_events.py     # GitHub webhook event models
│   └── queue/
│       ├── __init__.py
│       └── github_queue.py      # Queue management
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_work_item.py
│   └── test_queue.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .python-version
```

## Quick Start

### Using uv (recommended)

```bash
# Install dependencies
uv sync

# Run the notifier service
uv run python -m src.notifier_service

# Run the sentinel service
uv run python -m src.orchestrator_sentinel

# Run tests
uv run pytest
```

### Using Docker

```bash
# Build and run all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## API Endpoints

### Notifier Service (port 8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check endpoint |
| `/ready` | GET | Readiness check endpoint |

## Development

### Code Quality

```bash
# Format and lint
uv run ruff format .
uv run ruff check .

# Type checking
uv run mypy src/
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level |
| `SENTINEL_POLL_INTERVAL_SECONDS` | `30` | Sentinel polling interval |

## License

MIT License
