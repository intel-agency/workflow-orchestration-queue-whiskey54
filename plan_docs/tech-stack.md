# OS-APOW Technology Stack

**Application:** OS-APOW (Orchestrated Sentinel for Project Orchestration Workflow)  
**Repository:** intel-agency/workflow-orchestration-queue  
**Last Updated:** 2026-03-27

---

## Primary Languages

| Language | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.12+ | Primary language for Orchestrator, API Webhook receiver, and all system logic |
| **PowerShell Core (pwsh)** | 7.x | Shell Bridge scripts, Auth synchronization, cross-platform CLI |
| **Bash** | 5.x | Shell Bridge scripts, DevContainer lifecycle hooks |

---

## Web Framework & Runtime

| Component | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | Latest | High-performance async web framework for Webhook Notifier |
| **Uvicorn** | Latest | ASGI web server implementation for serving FastAPI application |
| **Pydantic** | Latest | Data validation, settings management, schema definitions |

---

## HTTP & Networking

| Component | Version | Purpose |
|-----------|---------|---------|
| **HTTPX** | Latest | Async HTTP client for GitHub REST API calls |
| **HMAC (stdlib)** | - | Cryptographic signature verification for webhooks |

---

## Package Management

| Component | Version | Purpose |
|-----------|---------|---------|
| **uv** | 0.10.9+ | Rust-based Python package manager (fast dependency resolution) |
| **pyproject.toml** | - | Project configuration, dependencies, metadata |
| **uv.lock** | - | Deterministic lockfile for exact package versions |

---

## Containerization & Infrastructure

| Component | Purpose |
|-----------|---------|
| **Docker** | Container runtime for worker isolation |
| **Docker Compose** | Multi-container orchestration |
| **DevContainers** | Reproducible development environment |
| **Docker Networks** | Network isolation for security |

---

## Agent Runtime & LLM

| Component | Version | Purpose |
|-----------|---------|---------|
| **opencode CLI** | 1.2.24+ | AI agent runtime for executing workflows |
| **GLM-5 (ZhipuAI)** | Latest | Primary LLM provider for agent reasoning |
| **Claude (optional)** | 3.5 Sonnet | Alternative LLM provider |

---

## State Management

| Component | Purpose |
|-----------|---------|
| **GitHub Issues** | Distributed state management ("Markdown as a Database") |
| **GitHub Labels** | Task state machine (agent:queued, agent:in-progress, etc.) |
| **GitHub Milestones** | Phase/epic tracking |
| **GitHub Projects** | Kanban-style progress visualization |

---

## Observability & Logging

| Component | Purpose |
|-----------|---------|
| **Python logging (stdlib)** | Structured logging via StreamHandler (stdout) |
| **Docker logs** | Container runtime log capture |
| **Heartbeat comments** | Periodic status updates on long-running tasks |

---

## Security Components

| Component | Purpose |
|-----------|---------|
| **HMAC SHA256** | Webhook signature verification |
| **Credential Scrubber** | Regex-based secret removal from public logs |
| **Ephemeral Credentials** | Temporary environment variable injection |
| **Network Isolation** | Segregated Docker networks |
| **Resource Constraints** | CPU/RAM limits (2 CPUs, 4GB RAM) |

---

## Development Tools

| Component | Purpose |
|-----------|---------|
| **gh CLI** | GitHub API interaction |
| **git** | Version control |
| **pytest** | Unit/integration testing (planned) |

---

## Instruction Modules (Markdown-based)

| Module | Purpose |
|--------|---------|
| `local_ai_instruction_modules/` | Decoupled workflow prompts for LLM agents |
| `create-app-plan.md` | Application planning instructions |
| `perform-task.md` | Feature implementation instructions |
| `analyze-bug.md` | Bug analysis and fix instructions |

---

## Required Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `GITHUB_TOKEN` | ✅ | GitHub App Installation Token |
| `GITHUB_ORG` | ✅ | Target GitHub organization |
| `SENTINEL_BOT_LOGIN` | ✅ | Bot account login for task assignment |
| `WEBHOOK_SECRET` | ✅ (Notifier) | HMAC secret for webhook validation |

---

## Simplifications Applied

The following simplifications from the Simplification Report have been applied:

| ID | Change |
|----|--------|
| S-3 | Reduced to 3 required env vars (hardcoded sensible defaults for tuning knobs) |
| S-4 | Hardcoded `ENV_RESET_MODE` to `"stop"` |
| S-5 | Single-repo polling only (cross-repo deferred to future phase) |
| S-7 | Removed IPv4 scrubbing from credential scrubber |
| S-8 | Removed "encrypted" qualifier from log storage |
| S-10 | Stdout-only logging (no file handler) |
| S-11 | Removed unused `raw_payload` field from WorkItem |

---

## Dependencies (pyproject.toml)

```toml
[project]
name = "workflow-orchestration-queue"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "httpx>=0.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
]
```

---

*This document is derived from: OS-APOW Architecture Guide v3.2, Development Plan v4.2, Implementation Specification v1.2, and Simplification Report v1.*
