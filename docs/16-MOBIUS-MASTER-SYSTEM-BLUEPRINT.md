# Möbius — Master System Blueprint / 莫比乌斯总系统蓝图

> Status: **Target Architecture / 终局架构基线**
>
> This document defines the long-term system shape of Möbius. It does not expand the current implementation gate; it defines what later stages are building toward.

## 1. Product Definition

**Möbius is an operating system for AI engineering teams.**

It coordinates capable agent runtimes, governs engineering stages, controls repository state, collects evidence, preserves institutional memory, and projects durable knowledge into Obsidian for human use.

The core thesis is:

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

Möbius is Codex-first, but not Codex-only. OpenAI Codex is the reference runtime. Hermes is the first planned additional runtime. Additional runtimes may be admitted only through an explicit compatibility and governance gate.

---

## 2. Six Control Planes

Möbius is organized as six cooperating planes rather than one monolithic agent.

### Plane A — Agent Runtime Plane

Provides agency and execution.

```text
AgentRuntime
├── CodexRuntime
├── HermesRuntime
└── FutureRuntime
```

Normalized capabilities:

```text
discover
read_context
attach
 dispatch
watch
interrupt
collect_result
capabilities
health
```

Runtime-specific APIs remain behind adapters.

### Plane B — Engineering Governance Plane

Provides organizational control.

```text
Project Registry
Role Registry
Task Contract Engine
Stage Gate Engine
Policy Engine
Permission Boundaries
Controller Decisions
```

A role is a governed engineering identity, not merely a model session.

### Plane C — Evidence Plane

Turns execution into inspectable facts.

```text
Diff
Changed Files
Tests
Coverage
Lint
Type Checks
Build
Migrations
Service Health
Runtime Events
CI
PR State
Security Findings
Contract Deviations
```

Evidence can be automated. Judgment cannot be silently delegated.

### Plane D — Repository Control Plane

Controls the code-state machine.

```text
repository inspect
branch/worktree provision
workspace-role binding
commit
push
PR create/update
CI observe
merge authorization
merge
post-merge synchronization
```

Merge authorization is state-bound. A review of PR head SHA `X` does not authorize SHA `Y`.

### Plane E — Knowledge & Memory Plane

Preserves engineering memory as structured machine-readable state.

```text
ArchitectureDecision
StageRecord
ControllerDecision
FailureRecord
RepairPattern
RuntimeCompatibilityFinding
EngineeringLesson
ResearchThread
ValueThread
ProjectHypothesis
```

This is the durable institutional memory of the AI engineering organization.

### Plane F — Human Knowledge Plane

Projects selected knowledge into Obsidian.

```text
Möbius Source of Truth
        ↓
Knowledge Projection Engine
        ↓
Obsidian-compatible Markdown
        ↓
Human reading / backlinks / annotations / synthesis
```

Obsidian is a first-class human interface, but not the runtime database.

---

## 3. The Möbius Loop

The product name reflects the desired engineering loop: execution, review, repository state, and knowledge feed continuously into the next stage.

```text
Requirement / Idea
      ↓
Architecture + Stage Contract
      ↓
Role + Runtime Resolution
      ↓
Bounded Task Dispatch
      ↓
Agent Execution
      ↓
Evidence Collection
      ↓
Controller Review
   ┌──┴───────────────┐
   │                  │
  FIX                PASS
   │                  │
   └→ Repair Loop     ↓
                 Merge Authorization
                      ↓
                Repository Merge
                      ↓
             Knowledge Extraction
                      ↓
              Obsidian Projection
                      ↓
               Next Stage Context
                      ↓
                ── continues ──
```

The loop is continuous, but authority is not circular: final stage admission remains explicit.

---

## 4. Runtime Strategy — Codex + Hermes

Möbius does not attempt to fuse runtimes internally. It standardizes the control contract around them.

Example:

```yaml
roles:
  controller:
    authority: final

  research:
    runtime: hermes
    permissions: read-heavy

  backend:
    runtime: codex
    workspace: worktrees/backend

  frontend:
    runtime: codex
    workspace: worktrees/frontend

  security-review:
    runtime: hermes
    permissions: review-only

  integration:
    runtime: codex
    workspace: worktrees/integration
```

Codex remains the reference implementation until its real end-to-end control loop passes validation. Hermes integration requires a dedicated research decision before implementation.

---

## 5. Canonical Task Contract

Every meaningful worker action should be reducible to a bounded contract:

```yaml
project: FlowTracer
stage: BE-7
role: backend
runtime: codex
objective: implement frozen BE-7 contract
scope:
  allowed_paths: []
  forbidden_paths: []
non_goals: []
permissions: []
acceptance: []
validation: []
evidence_required: []
failure_policy:
  F1: repair
  F2: runtime_adapter
  F3: controller_contract_review
  F4: architecture_stop_and_ADR
report_format: structured
```

This contract is the unit of work across all runtimes.

---

## 6. Canonical Stage State Machine

```text
PLANNED
  ↓
ADMITTED
  ↓
IMPLEMENTING
  ↓
SUBMITTED
  ↓
REVIEWING
  ├── FIX_REQUIRED ──→ IMPLEMENTING
  ├── BLOCKED
  └── PASS
        ↓
MERGE_AUTHORIZED
        ↓
MERGED
        ↓
KNOWLEDGE_CAPTURED
        ↓
CLOSED
```

`KNOWLEDGE_CAPTURED` is an explicit post-merge state: a stage is not fully closed until important decisions, failures, repairs and reusable lessons have been processed into durable memory.

---

## 7. Obsidian Contract

Default mode is one-way projection:

```text
Möbius → Obsidian
```

Recommended vault projection:

```text
Möbius/
├── Projects/
│   └── <project>/
│       ├── Overview.md
│       ├── Architecture/
│       ├── Stages/
│       ├── Decisions/
│       └── Failures-and-Fixes/
├── Engineering-Knowledge/
├── Runtime-Compatibility/
├── Research-Threads/
└── Value-Threads/
```

Projected notes should carry stable machine IDs and provenance metadata so humans can edit and link them without confusing the projection with the source of truth.

Future bidirectional editing is optional and must define:

- provenance;
- ownership;
- conflict resolution;
- write permissions;
- validation before structured-state mutation.

---

## 8. Repository + Knowledge Coupling

Repository events become knowledge triggers.

```text
PR merged
  ↓
Stage finalized
  ↓
Evidence frozen
  ↓
Decision summary generated
  ↓
Reusable failures/fixes extracted
  ↓
Knowledge objects updated
  ↓
Obsidian projection refreshed
```

This means the repository is not only the code history. Möbius converts code history into engineering memory.

---

## 9. External Control Surface

Target external control surface remains narrow and structured.

```text
project.list
project.state
role.list
role.resolve
runtime.list
runtime.health
agent.discover
agent.read
task.prepare
task.dispatch
task.status
task.interrupt
evidence.get
stage.get
stage.review
repo.state
repo.prepare
repo.pr
repo.ci
repo.merge_authorized
knowledge.query
knowledge.project
```

No unrestricted shell or unbounded repository mutation is exposed merely for convenience.

---

## 10. Ideal User Experience

The user should eventually operate at the level of intent and authority:

```text
User:
Continue FlowTracer.

Möbius:
Stage BE-7 admitted.
Backend role resolved to CodexRuntime.
Workspace prepared.
Task contract dispatched.
Execution completed.
Validation passed except one P2 issue.
Repair loop completed.
Controller review packet ready.

User:
Approve.

Möbius:
Approval bound to PR head SHA.
Merge completed.
Worktrees synchronized.
Stage evidence frozen.
Engineering memory extracted.
Obsidian project memory updated.
Next stage ready.
```

The system hides mechanical work without hiding consequential decisions.

---

## 11. Architecture Invariants

1. Controller remains final authority for stage admission and consequential merge/release decisions.
2. Agent runtime capability is separated from governance policy.
3. Runtime-specific models do not leak above adapters.
4. Task targeting is exact and auditable.
5. Evidence is correlated to the exact task, stage and repository state.
6. Merge authorization is invalidated by repository-state change.
7. Knowledge capture is durable and provenance-aware.
8. Obsidian is a projection/interface, not the authoritative runtime store.
9. New runtimes require explicit admission research.
10. Architecture changes require an ADR when frozen assumptions are invalidated.

---

## 12. Delivery Discipline

The target system is large; implementation remains incremental.

Current order remains:

```text
Codex discovery
→ read
→ resume
→ bounded dispatch
→ status
→ evidence
→ role registry
→ stage gate
→ MCP
→ Repository Control
→ Knowledge Memory / Obsidian projection
→ Hermes runtime admission
→ broader automation
```

The blueprint is ambitious by design; implementation gates remain conservative by design.
