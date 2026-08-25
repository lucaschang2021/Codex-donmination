# Möbius / 莫比乌斯

> **Operating System for AI Engineering Teams.**  
> **AI 软件工程团队操作系统。**

**Möbius** is a controller-first operating system for AI software engineering teams. It turns persistent coding agents and autonomous agent runtimes into a governed, observable, auditable and cumulative engineering organization.

It is **Codex-first, not Codex-only**: OpenAI Codex is the reference runtime, Hermes is the first planned additional runtime, and future runtimes may be admitted through a narrow `AgentRuntime` contract.

Möbius is not just an agent orchestrator, not just Git automation, and not just a dashboard. Its purpose is to connect **execution, governance, evidence, repository state and long-term knowledge** into one continuous engineering loop.

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

> [!IMPORTANT]
> Möbius is currently **pre-alpha / architecture-first**. The target architecture is intentionally documented ahead of implementation. The immediate engineering goal remains narrow: prove the real Codex control loop, pass Controller gates, then expand the proven control plane.

---

## Why Möbius?

AI coding tools are already powerful. The missing layer is the engineering organization around them.

Today a human often still has to:

```text
switch agent windows
copy task instructions
rebuild context
watch execution manually
inspect Git
run or verify tests
open/update PRs
relay review feedback
remember why decisions were made
clean up project knowledge later
```

Möbius moves those mechanics into a governed control system while preserving explicit judgment and authority.

The user should operate at the level of:

```text
intent
architecture
project
stage
risk
decision
```

—not at the level of repetitive orchestration chores.

---

# The Möbius Loop / 莫比乌斯闭环

```text
Requirement / Intent
        ↓
Architecture + Contract
        ↓
Stage Admission
        ↓
Role Resolution
        ↓
Agent Runtime
   ┌────┼──────────┐
   ▼    ▼          ▼
 Codex Hermes    Future
   └────┼──────────┘
        ↓
Bounded Execution
        ↓
Evidence
        ↓
Git / Worktree / PR / CI
        ↓
Controller Review
   ┌────┼──────┐
   ▼    ▼      ▼
 PASS  FIX   BLOCK
   │    │
   │    └────────→ Repair Loop
   ▼
State-bound Merge Authorization
        ↓
Merge + Synchronization
        ↓
Knowledge Extraction
        ↓
Obsidian Projection
        ↓
Reusable Project Memory
        ↓
Next Stage / Requirement
        └──────────────────────────────→
```

The output of one stage becomes reliable context for the next. That continuous governed loop is the core idea behind the name **Möbius**.

---

# Six System Planes / 六大系统平面

## 1. Agent Runtime Plane

Agent runtimes provide **agency**: reasoning, planning, coding, tool use, recovery and execution.

```text
AgentRuntime
├── CodexRuntime      # reference implementation
├── HermesRuntime     # planned second runtime
└── FutureRuntime     # explicit admission only
```

Normalized capability contract:

```text
discover()
read_context()
attach()
dispatch()
watch()
interrupt()
collect_result()
capabilities()
```

Runtime-specific concepts stay behind adapters. Upper-layer governance must not depend on Codex thread internals or Hermes session internals.

## 2. Orchestration Plane

Möbius turns anonymous agents into explicit engineering roles.

```text
Project Registry
Role Registry
Runtime Routing
Context Packager
Task Contract Engine
Cross-role Handoff
Repair Loop Router
```

Example roles:

```text
Controller
Backend
Frontend
Integration
Research
Security Review
Release / GitHub
```

A role may bind an exact runtime identity, workspace/worktree, allowed paths, forbidden actions, validation profile and escalation policy.

## 3. Governance Plane

Möbius encodes the engineering constitution.

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
  ├── FIX_REQUIRED → IMPLEMENTING
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

Worker completion is not Controller approval. A worker cannot silently admit the next stage or inherit merge authority.

## 4. Evidence Plane

Möbius separates what an agent *claims* from what the system can *prove*.

Candidate evidence:

```text
git diff / changed files
tests / coverage
lint / type checks
build / migrations
Docker / service health
runtime errors
CI checks
PR state
security checks
contract deviations
execution metadata
```

Canonical output:

```text
ValidationManifest
```

> **Automate evidence, not judgment.**

## 5. Repository Plane

Git and GitHub become governed infrastructure rather than manual chores.

Target capabilities:

```text
repository inspection
branch creation / reuse
worktree lifecycle
workspace-role binding
clean-worktree guards
commit / push
PR creation / update
CI observation
merge authorization validation
merge
post-merge synchronization
```

The intended flow:

```text
Agent completes bounded work
→ evidence collected
→ commit / push / PR
→ CI
→ Controller review
→ PASS
→ merge authorization bound to exact PR head SHA
→ merge
→ synchronize main + worktrees
```

If the reviewed repository state changes, the previous authorization becomes invalid.

**Git mechanics may be automated. Git authority remains explicit.**

## 6. Knowledge Plane

Möbius treats engineering memory as a first-class output.

Machine-readable knowledge remains owned by Möbius:

```text
Project Memory
Architecture Decisions
Stage Records
Failure / Fix Knowledge
Runtime Compatibility Knowledge
Engineering Patterns
Research Threads
Value Threads
```

Human-facing projection:

```text
Möbius Source of Truth
        ↓
Knowledge Extraction
        ↓
Knowledge Projection Engine
        ↓
Obsidian-compatible Markdown
        ↓
Backlinks / Maps of Content / Human Annotation
```

Obsidian is a **first-class Human Knowledge Interface**, not a runtime database and not an implicit authority source.

Default direction:

```text
Möbius → Obsidian
```

A future bidirectional mode requires explicit provenance, conflict-resolution and permission rules.

---

# Codex + Hermes

Möbius does not fuse Codex and Hermes into one giant agent implementation. Both plug into the same engineering governance system.

```text
                     Controller
                         │
                    Stage Gate
                         │
                  Role Resolution
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Backend Role             Research Role
        CodexRuntime            HermesRuntime
             │                       │
             └───────────┬───────────┘
                         ▼
                  Evidence Engine
                         │
                 Repository Control
                         │
                      PR / CI
                         │
                 Controller Review
                         │
                 Knowledge Extraction
                         │
                      Obsidian
```

### CodexRuntime

Codex is the reference implementation and first product proof. The initial product is built around real persistent Codex engineering workflows: discovery, context read, resume, bounded dispatch and execution status.

### HermesRuntime

Hermes is the first planned non-Codex runtime. It is expected to complement Codex in research, planning, autonomous investigation, review/security assistance and specialized recovery workflows.

Hermes integration is **planned**, not claimed as already implemented. It must pass a dedicated integration research / ADR gate before admission.

---

# Bounded Task Contracts

Workers receive explicit engineering contracts rather than vague open-ended prompts.

```text
Project
Version
Stage
Role
Runtime
Objective
Frozen Scope
Non-goals
Allowed Files / Workspace
Permission Boundary
Acceptance Criteria
Required Validation
Evidence Requirements
Failure Rules
Report Format
```

This contract is runtime-independent.

Failure model:

```text
F1 — Implementation defect
     → repair inside current stage

F2 — Runtime / compatibility defect
     → repair runtime adapter

F3 — Contract defect
     → Controller updates contract / ADR

F4 — Architecture invalidated
     → stop, issue ADR, explicitly redesign
```

Implementation bugs do not silently redefine architecture.

---

# Obsidian Knowledge Architecture

The engineering loop should not end at `merged`.

A mature stage closes like this:

```text
Stage execution completes
        ↓
Evidence finalized
        ↓
Controller decision recorded
        ↓
Repository state finalized
        ↓
Knowledge extracted
        ↓
Project Memory + Engineering Knowledge + Research/Value Threads
        ↓
Obsidian projection
        ↓
Next stage reuses proven knowledge
```

Suggested vault structure:

```text
Möbius Vault/
├── Projects/
├── Architecture/
├── ADR/
├── Stages/
├── Failures-and-Fixes/
├── Engineering-Knowledge/
├── Runtime-Knowledge/
├── Research/
├── Value-Threads/
├── Decisions/
└── Indexes/
```

Generated notes should carry provenance such as project, stage, runtime, commit, PR and creation time, while generated content remains distinguishable from human annotations.

---

# Ideal Experience / 理想体验

```text
You:
Continue FlowTracer.

Möbius:
Current stage: BE-7.
Backend role resolved to CodexRuntime.
Frozen contract loaded.
Worktree prepared.
Task dispatched.
Implementation completed.
82 tests passed.
CI passed.
1 P2 issue found during independent review.
Repair task returned to Backend.
Second validation passed.
Awaiting merge authorization.

After approval:
PR head verified.
Merge completed.
Main and worktrees synchronized.
Stage record finalized.
Engineering knowledge extracted.
Obsidian project memory updated.
Next stage ready for admission.
```

That is the intended product experience: the human directs the engineering system; Möbius handles the controlled loop beneath it.

---

# Roadmap / v0.1 → v1.1

| Version | Target |
|---|---|
| **v0.1** | Codex persistent-thread discovery foundation |
| **v0.2** | structured thread/context read |
| **v0.3** | resume / persistent attachment |
| **v0.4** | bounded task dispatch |
| **v0.5** | normalized execution status |
| **v0.6** | evidence / validation manifests |
| **v0.7** | role registry + project bindings |
| **v0.8** | executable Stage Gate methodology |
| **v0.9** | minimal MCP control surface |
| **v1.0** | complete Codex-first engineering control plane |
| **v1.1** | Repository Control + workflow automation + Knowledge Projection + Hermes/multi-runtime admission path |

The implementation stays **Codex-first**. The architecture is broad; the execution plan stays disciplined.

---

# Documentation

The canonical architecture is defined before heavy implementation so coding agents execute bounded stages instead of redesigning the system during construction.

- [`docs/00-PROJECT-CONTROL.md`](./docs/00-PROJECT-CONTROL.md) — governance baseline
- [`docs/02-R0-INTEGRATION-DECISION.md`](./docs/02-R0-INTEGRATION-DECISION.md) — Codex integration decision
- [`docs/10-MASTER-TECHNICAL-DESIGN.md`](./docs/10-MASTER-TECHNICAL-DESIGN.md) — original master technical baseline
- [`docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md`](./docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md) — versioned construction plan
- [`docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md`](./docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md) — Repository Control architecture
- [`docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md`](./docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md) — multi-runtime architecture
- [`docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md`](./docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md) — naming + knowledge architecture
- [`docs/16-MOBIUS-CANONICAL-MASTER-ARCHITECTURE.md`](./docs/16-MOBIUS-CANONICAL-MASTER-ARCHITECTURE.md) — **canonical target system architecture**

---

# Current Status

**Pre-alpha / architecture-first implementation.**

Current engineering priority:

```text
Codex v0.1
→ discover real persistent threads
→ validate on a real local Codex environment
→ Controller gate
→ read / resume / dispatch / status
```

Repository Control, Knowledge Projection, Hermes and broader automation are part of the target system, but they do not bypass the stage-gated Codex foundation.

The official product name is **Möbius / 莫比乌斯**. `Codex Domination` is retained only as the historical codename/origin.

---

# License

MIT License. See [`LICENSE`](./LICENSE).
