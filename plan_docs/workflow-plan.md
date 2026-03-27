# **Workflow Execution Plan: project-setup**

## **1. Overview**

| Field | Value |
|-------|-------|
| **Workflow Name** | `project-setup` |
| **Workflow File** | `ai_instruction_modules/ai-workflow-assignments/dynamic-workflows/project-setup.md` |
| **Project Name** | `workflow-orchestration-queue` |
| **Repository** | `intel-agency/workflow-orchestration-queue-whiskey54` |
| **Total Assignments** | 6 main + 3 event assignments = 9 total |
| **Current Event** | `pre-script-begin` |

### High-Level Summary

The `project-setup` dynamic workflow transforms a template repository clone into a fully initialized project environment. It creates the foundational infrastructure (branch, project, labels), produces a comprehensive application plan based on the seeded planning documents, scaffolds the actual project structure, creates agent documentation, captures learnings, and merges the setup PR.

**Key Directive:** All GitHub Actions workflows created or modified during this workflow MUST pin actions to specific commit SHAs (not version tags).

---

## **2. Project Context Summary**

### Application Overview

**workflow-orchestration-queue** is a headless agentic orchestration platform that transforms GitHub Issues into "Execution Orders" autonomously fulfilled by specialized AI agents. It shifts from interactive AI coding to a persistent, event-driven background service.

### Technology Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.12+ |
| **Web Framework** | FastAPI + Uvicorn |
| **Validation** | Pydantic |
| **HTTP Client** | httpx (async) |
| **Package Manager** | uv (Rust-based) |
| **Containerization** | Docker + DevContainer |
| **Agent Runtime** | opencode CLI |
| **LLM Provider** | ZhipuAI GLM-5 |
| **State Management** | GitHub Issues + Labels |

### 4-Pillar Architecture

1. **The Ear (Notifier)**: FastAPI webhook receiver with HMAC validation
2. **The State (Queue)**: GitHub Issues as database ("Markdown as a Database")
3. **The Brain (Sentinel)**: Persistent polling orchestrator with shell-bridge execution
4. **The Hands (Worker)**: opencode DevContainer for code execution

### Phased Rollout

- **Phase 0**: Manual seeding (template clone + plan docs)
- **Phase 1**: Sentinel MVP (polling, shell-bridge, label management)
- **Phase 2**: The Ear (webhook automation, template triage)
- **Phase 3**: Deep Orchestration (hierarchical decomposition, self-healing)

### Key Constraints & Decisions (from Simplification Report)

- **3 env vars only**: `GITHUB_TOKEN`, `GITHUB_ORG`, `SENTINEL_BOT_LOGIN`
- **Env reset mode**: Hardcoded to `"stop"` between tasks
- **Polling scope**: Single-repo only (cross-repo deferred)
- **Queue abstraction**: `ITaskQueue` retained for future provider swapping
- **Logging**: stdout only (no file handler)

### Known Risks (from Plan Review)

| Risk | Mitigation |
|------|------------|
| Race conditions in task claiming | Assign-then-verify pattern |
| No heartbeat implementation | Background async coroutine (to be implemented) |
| `httpx.AsyncClient` per-call | Connection pooling needed |
| Hardcoded secrets in notifier scaffold | Environment variable validation |

---

## **3. Assignment Execution Plan**

### Assignment 1: `create-workflow-plan` *(Current)*

| Field | Content |
|-------|---------|
| **Goal** | Create a comprehensive workflow execution plan for the project-setup dynamic workflow |
| **Key Acceptance Criteria** | • Dynamic workflow file read and understood<br>• All referenced assignments traced and read<br>• All plan_docs/ files read<br>• Plan produced with assignment order, dependencies, risks<br>• Plan presented and approved by stakeholder<br>• Committed to `plan_docs/workflow-plan.md` |
| **Project-Specific Notes** | This is a template repo with existing structure. The plan must account for existing files (AGENTS.md, workflows, devcontainer configs) that may be enhanced rather than replaced. |
| **Prerequisites** | Access to remote `nam20485/agent-instructions` repository for assignment resolution |
| **Dependencies** | None (first event) |
| **Risks / Challenges** | Assignment files must be fetched from remote repository; 404 errors may occur if paths differ |
| **Events** | None |

---

### Assignment 2: `init-existing-repository`

| Field | Content |
|-------|---------|
| **Goal** | Initialize the existing repository by creating branch, project, labels, and PR |
| **Key Acceptance Criteria** | • New branch `dynamic-workflow-project-setup` created FIRST<br>• Branch protection ruleset imported from `.github/protected-branches_ruleset.json`<br>• GitHub Project created with columns (Not Started, In Progress, In Review, Done)<br>• Labels imported from `.github/.labels.json`<br>• Workspace/devcontainer files renamed to match project<br>• PR created from branch to `main` |
| **Project-Specific Notes** | Template repo already has `.github/.labels.json` and `.github/protected-branches_ruleset.json`. Must verify PAT has `administration: write` scope for ruleset import. Use `GH_ORCHESTRATION_AGENT_TOKEN` (not `GITHUB_TOKEN`). |
| **Prerequisites** | GitHub authentication with scopes: `repo`, `project`, `read:project`, `read:user`, `user:email`, `administration: write` |
| **Dependencies** | None (first main assignment) |
| **Risks / Challenges** | • Ruleset import may fail if PAT lacks `administration: write`<br>• PR creation requires at least one commit on branch<br>• Project creation requires `project` scope |
| **Events** | None declared |

---

### Assignment 3: `create-app-plan`

| Field | Content |
|-------|---------|
| **Goal** | Create a comprehensive application plan based on the filled-out app template and supporting documents |
| **Key Acceptance Criteria** | • Application template thoroughly analyzed<br>• Plan documented in issue using Appendix A template<br>• All phases with steps documented<br>• Tech stack, components, dependencies planned<br>• Risks and mitigations identified<br>• Issue created, linked to GitHub Project, assigned to milestone<br>• Labels applied (`planning`, `documentation`) |
| **Project-Specific Notes** | Plan docs are comprehensive (Architecture Guide v3.2, Development Plan v4.2, Implementation Spec v1.2, Plan Review, Simplification Report). The plan should synthesize these into an actionable implementation roadmap. Note: `orchestration:plan-approved` label is applied by `post-script-complete` event, NOT by this assignment. |
| **Prerequisites** | GitHub Project exists (from `init-existing-repository`) |
| **Dependencies** | `init-existing-repository` (for project, labels, milestones) |
| **Risks / Challenges** | • Plan docs are extensive; must synthesize without losing critical details<br>• Milestones must align with 4 phases defined in Development Plan |
| **Events** | `pre-assignment-begin`: gather-context<br>`on-assignment-failure`: recover-from-error<br>`post-assignment-complete`: report-progress |

---

### Assignment 4: `create-project-structure`

| Field | Content |
|-------|---------|
| **Goal** | Create the actual project structure and scaffolding based on the application plan |
| **Key Acceptance Criteria** | • Solution/project structure created following tech stack<br>• All project files and directories established<br>• Dockerfile, docker-compose.yml, config files created<br>• CI/CD pipeline structure established<br>• Documentation structure created<br>• Repository summary (`.ai-repository-summary.md`) created<br>• All GitHub Actions pinned to commit SHAs<br>• Stakeholder approval obtained |
| **Project-Specific Notes** | Tech stack is Python 3.12+ with uv, FastAPI, Pydantic, httpx. Structure should follow the Implementation Spec: `src/` with `notifier_service.py`, `orchestrator_sentinel.py`, `models/`, `queue/`. Docker healthchecks must use Python stdlib (no curl). Editable installs (`uv pip install -e .`) require `COPY src/` before install. |
| **Prerequisites** | Application plan exists (from `create-app-plan`) |
| **Dependencies** | `create-app-plan` (for plan context, tech stack, architecture) |
| **Risks / Challenges** | • Existing template files may conflict with new structure<br>• Docker healthcheck syntax (use Python, not curl)<br>• CI workflow actions must be SHA-pinned |
| **Events** | None declared |

---

### Assignment 5: `create-agents-md-file`

| Field | Content |
|-------|---------|
| **Goal** | Create a comprehensive `AGENTS.md` file at repository root for AI coding agents |
| **Key Acceptance Criteria** | • `AGENTS.md` exists at repository root<br>• Contains project overview, tech stack<br>• Setup/build/test commands verified to work<br>• Code style conventions documented<br>• Project structure / directory layout documented<br>• Testing instructions included<br>• PR/commit guidelines included<br>• All commands validated by running them<br>• Committed to working branch |
| **Project-Specific Notes** | Template repo already has `AGENTS.md`. This assignment should **enhance** the existing file with project-specific details (Python stack, uv commands, Docker/DevContainer setup, Sentinel/Notifier architecture). Cross-reference with README.md and `.ai-repository-summary.md`. |
| **Prerequisites** | Project structure exists (from `create-project-structure`) |
| **Dependencies** | `create-project-structure` (for actual commands to validate) |
| **Risks / Challenges** | • Must run actual build/test commands to validate<br>• Existing AGENTS.md content should be preserved/enhanced, not replaced |
| **Events** | None declared |

---

### Assignment 6: `debrief-and-document`

| Field | Content |
|-------|---------|
| **Goal** | Capture key learnings, insights, and areas for improvement from the setup workflow |
| **Key Acceptance Criteria** | • Detailed report created using structured template (12 sections)<br>• All deviations from assignments documented<br>• Execution trace saved as `debrief-and-document/trace.md`<br>• Report reviewed and approved by stakeholders<br>• Committed and pushed to repo |
| **Project-Specific Notes** | Must flag any plan-impacting findings as ACTION ITEMS. For each, recommend filing a new issue or updating phase/epic descriptions. Review upcoming steps for continued validity given what was learned. |
| **Prerequisites** | All main assignments completed |
| **Dependencies** | All prior assignments (for complete trace) |
| **Risks / Challenges** | • Long workflow may have many items to capture<br>• Must ensure action items are filed as GitHub issues |
| **Events** | None declared |

---

### Assignment 7: `pr-approval-and-merge`

| Field | Content |
|-------|---------|
| **Goal** | Complete the full PR approval and merge process for the setup branch |
| **Key Acceptance Criteria** | • All CI/CD status checks pass before code review<br>• CI remediation loop executed (up to 3 attempts)<br>• Code review delegated to `code-reviewer` subagent (NOT self-review)<br>• Auto-reviewer comments waited for<br>• `ai-pr-comment-protocol.md` workflow executed<br>• All review comments resolved via GraphQL<br>• Stakeholder approval obtained<br>• PR merged, source branch deleted<br>• Related issues closed |
| **Project-Specific Notes** | This is an automated setup PR — self-approval by orchestrator is acceptable per workflow spec. However, the CI remediation loop MUST still be executed. PR number comes from `init-existing-repository` output (`#initiate-new-repository.init-existing-repository`). |
| **Prerequisites** | PR exists with all changes committed |
| **Dependencies** | `init-existing-repository` (for `$pr_num`), all other assignments (for complete changes) |
| **Risks / Challenges** | • CI may fail on initial run (lint, scan, test)<br>• Must commit all changes before merge<br>• GraphQL verification artifacts required |
| **Events** | None declared |
| **Input** | `$pr_num` from `init-existing-repository` |
| **Output** | `result`: `"merged"` | `"pending"` | `"failed"` |

---

### Post-Assignment Event Assignments

These run after each main assignment completes:

#### `validate-assignment-completion`

| Field | Content |
|-------|---------|
| **Goal** | Validate that a completed assignment has met all acceptance criteria |
| **Key Acceptance Criteria** | • All required files exist<br>• All verification commands pass<br>• Validation report created<br>• Pass/fail determined<br>• Remediation steps provided if failed |
| **Execution** | Runs after each main assignment in the `post-assignment-complete` event |
| **Risks** | Must be delegated to independent QA agent (`qa-test-engineer`) |

#### `report-progress`

| Field | Content |
|-------|---------|
| **Goal** | Provide progress reporting after each workflow step completes |
| **Key Acceptance Criteria** | • Structured progress report generated<br>• Step outputs captured<br>• Validation checks passed<br>• Workflow state checkpointed<br>• Action items filed as GitHub issues |
| **Execution** | Runs after each main assignment in the `post-assignment-complete` event |
| **Risks** | All identified items MUST be filed as GitHub issues |

---

### Post-Script-Complete Event

After all assignments complete successfully:

| Action | Description |
|--------|-------------|
| **Apply Label** | Apply `orchestration:plan-approved` to the application plan issue (created in `create-app-plan`) |
| **Location** | Issue recorded as `#initiate-new-repository.create-app-plan` |
| **Purpose** | Signals that the plan is ready for epic creation, triggering the next orchestration pipeline phase |

---

## **4. Sequencing Diagram**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROJECT-SETUP WORKFLOW EXECUTION                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─ PRE-SCRIPT-BEGIN EVENT ────────────────────────────────────────────────┐
│                                                                          │
│  ┌─────────────────────────┐                                            │
│  │ create-workflow-plan    │ ──→ plan_docs/workflow-plan.md            │
│  │ (COMPLETE)              │                                            │
│  └─────────────────────────┘                                            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─ MAIN ASSIGNMENTS ──────────────────────────────────────────────────────┐
│                                                                          │
│  ┌─────────────────────────┐                                            │
│  │ 1. init-existing-repo   │ ──→ Branch, Project, Labels, PR           │
│  └───────────┬─────────────┘                                            │
│              │                                                           │
│              ▼                                                           │
│  ┌─────────────────────────┐                                            │
│  │ 2. create-app-plan      │ ──→ Plan Issue, Milestones                 │
│  └───────────┬─────────────┘                                            │
│              │                                                           │
│              ▼                                                           │
│  ┌─────────────────────────┐                                            │
│  │ 3. create-project-      │ ──→ Scaffolding, CI/CD, Docker            │
│  │    structure            │                                            │
│  └───────────┬─────────────┘                                            │
│              │                                                           │
│              ▼                                                           │
│  ┌─────────────────────────┐                                            │
│  │ 4. create-agents-md     │ ──→ AGENTS.md (enhanced)                   │
│  └───────────┬─────────────┘                                            │
│              │                                                           │
│              ▼                                                           │
│  ┌─────────────────────────┐                                            │
│  │ 5. debrief-and-document │ ──→ Debrief Report, Trace                  │
│  └───────────┬─────────────┘                                            │
│              │                                                           │
│              ▼                                                           │
│  ┌─────────────────────────┐                                            │
│  │ 6. pr-approval-and-     │ ──→ Merged PR, Closed Issues              │
│  │    merge                │                                            │
│  └─────────────────────────┘                                            │
│                                                                          │
│  ┌─ AFTER EACH MAIN ASSIGNMENT ─────────────────────────────────────┐   │
│  │                                                                   │   │
│  │  validate-assignment-completion → report-progress                │   │
│  │                                                                   │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─ POST-SCRIPT-COMPLETE EVENT ────────────────────────────────────────────┐
│                                                                          │
│  Apply `orchestration:plan-approved` to plan issue                      │
│  → Triggers next orchestration pipeline phase                           │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## **5. Open Questions**

| # | Question | Context | Recommended Resolution |
|---|----------|---------|------------------------|
| 1 | **Existing AGENTS.md handling** | Template repo already has AGENTS.md. Should `create-agents-md-file` enhance or replace? | **Enhance** - Preserve existing content, add project-specific sections |
| 2 | **Branch protection ruleset import** | Requires `administration: write` scope. Has this been verified? | Run `./scripts/test-github-permissions.ps1` before `init-existing-repository` |
| 3 | **GitHub Project name** | Should project match repo name exactly or use a different naming convention? | Use repo name as specified in `init-existing-repository` |
| 4 | **Milestone alignment** | Plan docs describe 4 phases. Should milestones map 1:1 to phases? | Yes - Create milestones: "Phase 1: Foundation", "Phase 2: The Ear", "Phase 3: Deep Orchestration" |
| 5 | **CI workflow SHA pinning** | Existing workflows may have tag references. Should they be updated during `create-project-structure`? | Yes - All workflows must have SHA-pinned actions per workflow directive |

---

## **6. Files Referenced**

| File | Source | Purpose |
|------|--------|---------|
| `ai_instruction_modules/ai-workflow-assignments/dynamic-workflows/project-setup.md` | Remote | Dynamic workflow definition |
| `plan_docs/OS-APOW Architecture Guide v3.2.md` | Local | Architecture reference |
| `plan_docs/OS-APOW Development Plan v4.2.md` | Local | Development phases, user stories |
| `plan_docs/OS-APOW Implementation Specification v1.2.md` | Local | Tech stack, requirements, acceptance criteria |
| `plan_docs/OS-APOW Plan Review.md` | Local | Issues, gotchas, recommendations |
| `plan_docs/OS-APOW Simplification Report v1.md` | Local | Applied simplifications, decisions |
| `.github/.labels.json` | Local | Label definitions for import |
| `.github/protected-branches_ruleset.json` | Local | Branch protection ruleset |

---

## **7. Stakeholder Approval**

**Status:** ✅ Approved

> **Approval Statement:**
> This workflow execution plan has been reviewed and approved by the orchestrator. The plan accurately reflects the project context, assignment order, dependencies, and risks. Open questions are noted and will be addressed during execution.

---

**Plan Prepared By:** Planner Agent  
**Date:** 2026-03-27  
**Workflow:** `project-setup`  
**Repository:** `intel-agency/workflow-orchestration-queue-whiskey54`
