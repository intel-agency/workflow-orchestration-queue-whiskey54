# OS-APOW Architecture Overview

**Application:** OS-APOW (Orchestrated Sentinel for Project Orchestration Workflow)  
**Repository:** intel-agency/workflow-orchestration-queue  
**Last Updated:** 2026-03-27

---

## Executive Summary

OS-APOW (workflow-orchestration-queue) represents a paradigm shift from **Interactive AI Coding** to **Headless Agentic Orchestration**. It transforms standard project management artifacts (GitHub Issues) into "Execution Orders" autonomously fulfilled by specialized AI agents, moving the agent from a passive co-pilot role to a background production service.

The system is designed to be **Self-Bootstrapping** — once the initial deployment is seeded from the template repository, the system uses its own orchestration capabilities to refine its components.

---

## 4-Pillar Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OS-APOW System Architecture                          │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   GitHub Events  │
                    │  (Webhook/API)   │
                    └────────┬─────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              THE EAR (Notifier)                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ FastAPI Webhook Receiver                                             │    │
│  │ • HMAC SHA256 validation                                             │    │
│  │ • Event parsing & triage                                             │    │
│  │ • WorkItem manifest generation                                       │    │
│  │ • Queue initialization (agent:queued label)                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            THE STATE (Work Queue)                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ GitHub Issues as Database ("Markdown as a Database")                 │    │
│  │ • Labels: agent:queued → agent:in-progress → agent:success/error    │    │
│  │ • Assignees: Distributed locking mechanism                           │    │
│  │ • Comments: Heartbeat & status updates                               │    │
│  │ • Milestones: Phase/epic tracking                                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         THE BRAIN (Sentinel Orchestrator)                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Python Async Background Service                                      │    │
│  │ • Polling engine (60s interval, jittered backoff)                    │    │
│  │ • Task claiming (assign-then-verify pattern)                         │    │
│  │ • Shell-Bridge dispatch (devcontainer-opencode.sh)                   │    │
│  │ • Status management (label transitions, comments)                    │    │
│  │ • Heartbeat coroutine (5-minute intervals)                           │    │
│  │ • Graceful shutdown (SIGTERM/SIGINT handling)                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          THE HANDS (Opencode Worker)                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ DevContainer Environment                                             │    │
│  │ • Isolated Docker network                                            │    │
│  │ • opencode CLI runtime                                               │    │
│  │ • LLM reasoning (GLM-5 / Claude)                                     │    │
│  │ • Markdown instruction modules                                       │    │
│  │ • Local test execution                                               │    │
│  │ • PR creation & submission                                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Services

### 1. Work Event Notifier (`src/notifier_service.py`)

**Role:** The system's primary gateway for external stimuli.

**Responsibilities:**
- Secure webhook ingestion at `/webhooks/github`
- HMAC SHA256 signature verification
- Event parsing and intelligent triage
- WorkItem manifest generation
- Queue initialization via `agent:queued` label

**Technology:** FastAPI + Uvicorn + Pydantic

### 2. Sentinel Orchestrator (`src/orchestrator_sentinel.py`)

**Role:** Persistent supervisor managing worker lifecycle.

**Responsibilities:**
- Polling GitHub Issues API every 60 seconds
- Task claiming with assign-then-verify locking
- Shell-Bridge dispatch to DevContainer
- Status feedback (labels, comments, heartbeats)
- Graceful shutdown handling

**Technology:** Python async (asyncio) + HTTPX + subprocess

### 3. Shared Models (`src/models/`)

**Components:**
- `work_item.py`: Unified WorkItem, TaskType, WorkItemStatus, scrub_secrets()
- `github_events.py`: Schemas for GitHub webhook payloads

### 4. Queue Interface (`src/queue/`)

**Components:**
- `github_queue.py`: ITaskQueue ABC + GitHubQueue implementation
- Shared by both Sentinel and Notifier

---

## Data Flow (Happy Path)

```
1. User opens GitHub Issue with [Application Plan] template
                    │
                    ▼
2. GitHub Webhook hits Notifier (FastAPI)
                    │
                    ▼
3. Notifier verifies HMAC signature, parses issue
                    │
                    ▼
4. Notifier applies agent:queued label via GitHub API
                    │
                    ▼
5. Sentinel poller discovers queued issue
                    │
                    ▼
6. Sentinel claims task (assign-then-verify)
                    │
                    ▼
7. Sentinel updates label to agent:in-progress
                    │
                    ▼
8. Sentinel runs git clone/pull on target repo
                    │
                    ▼
9. Sentinel executes devcontainer-opencode.sh up
                    │
                    ▼
10. Sentinel dispatches prompt via devcontainer-opencode.sh
                    │
                    ▼
11. Worker (opencode) executes task in DevContainer
                    │
                    ▼
12. Worker creates branch, writes code, runs tests
                    │
                    ▼
13. Worker creates PR linking to original issue
                    │
                    ▼
14. Sentinel detects completion, applies agent:success
```

---

## State Machine (Label Logic)

```
                    ┌─────────────────┐
                    │  (Issue Opened) │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  agent:queued   │  ← Task awaiting pickup
                    └────────┬────────┘
                             │ Sentinel claims
                             ▼
               ┌─────────────────────────┐
               │  agent:in-progress      │  ← Task being executed
               └────────────┬────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
   ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐
   │agent:success│  │ agent:error │  │agent:infra-failure│
   │  (PR ready) │  │ (impl fail) │  │  (infra fail)    │
   └─────────────┘  └─────────────┘  └─────────────────┘
```

**Special States:**
- `agent:reconciling`: Stale task recovery (stuck in-progress > timeout)
- `agent:stalled-budget`: Cost guardrails triggered (future feature)

---

## Key Architectural Decisions

### ADR 07: Standardized Shell-Bridge Execution

**Decision:** Orchestrator interacts with agentic environment exclusively via `./scripts/devcontainer-opencode.sh`.

**Rationale:** Reuses existing shell infrastructure for Docker logic, SSH-agent forwarding, volume mounts. Prevents "Configuration Drift" between AI and human environments.

### ADR 08: Polling-First Resiliency Model

**Decision:** Sentinel uses polling as primary discovery; webhooks are optimization.

**Rationale:** Webhooks are "fire and forget" — if server is down during event, event is lost. Polling ensures self-healing via state reconciliation on restart.

### ADR 09: Provider-Agnostic Interface Layer

**Decision:** Queue interactions abstracted behind `ITaskQueue` interface.

**Rationale:** Enables future swapping to Linear, Notion, or SQL queues without rewriting orchestrator logic.

---

## Security Architecture

### Network Isolation
- Worker containers run in dedicated Docker network
- Cannot access host network or local subnet
- Internet access for packages only

### Credential Management
- GitHub tokens injected as temporary environment variables
- Destroyed when container exits
- Never written to disk

### Credential Scrubbing
- All log output passed through `scrub_secrets()` before GitHub comments
- Strips patterns: `ghp_*`, `ghs_*`, `gho_*`, `github_pat_*`, `Bearer`, `sk-*`, ZhipuAI keys

### Resource Constraints
- Worker containers: 2 CPUs, 4GB RAM hard cap
- Prevents DoS from rogue agents

---

## Project Structure

```
workflow-orchestration-queue/
├── pyproject.toml               # uv dependencies and metadata
├── uv.lock                      # Deterministic lockfile
├── src/
│   ├── notifier_service.py      # FastAPI webhook receiver
│   ├── orchestrator_sentinel.py # Background polling service
│   ├── models/
│   │   ├── work_item.py         # Unified WorkItem model
│   │   └── github_events.py     # Webhook payload schemas
│   └── queue/
│       └── github_queue.py      # ITaskQueue + GitHubQueue
├── scripts/
│   ├── devcontainer-opencode.sh # Shell-Bridge execution
│   ├── gh-auth.ps1              # GitHub auth sync
│   └── update-remote-indices.ps1# Vector index maintenance
├── local_ai_instruction_modules/# Markdown workflow prompts
└── docs/                        # Documentation
```

---

## Phased Rollout

| Phase | Name | Focus | Status |
|-------|------|-------|--------|
| **0** | Seeding | Manual template clone, env setup | Bootstrap |
| **1** | The Sentinel | Polling, shell-bridge, status feedback | MVP |
| **2** | The Ear | Webhook receiver, intelligent triage | Enhancement |
| **3** | Deep Orchestration | Hierarchical decomposition, self-healing | Advanced |

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| GitHub API Rate Limiting | GitHub App tokens (5,000 req/hr); aggressive caching |
| LLM Looping/Hallucination | Max steps timeout; cost guardrails; retry counter |
| Concurrency Collisions | Assign-then-verify pattern; distributed locking |
| Container Drift | Stop container between tasks; fast restart |
| Security Injection | HMAC validation; credential scrubbing; network isolation |

---

*This document is derived from: OS-APOW Architecture Guide v3.2, Development Plan v4.2, Implementation Specification v1.2, and Plan Review.*
