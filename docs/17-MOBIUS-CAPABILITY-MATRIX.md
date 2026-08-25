# Möbius — Capability Matrix / 能力矩阵

> Purpose: turn the end-state architecture into a concrete capability map without changing current stage admission.

## 1. Core capability domains

| Domain | Capability | Target behavior | Authority boundary |
|---|---|---|---|
| Runtime | Discover agents | enumerate persistent or addressable agents | read-only |
| Runtime | Read context | inspect structured history/state | read-only |
| Runtime | Attach/resume | reconnect to persistent context | explicit target |
| Runtime | Dispatch | send bounded work contract | stage/role permission |
| Runtime | Observe | stream normalized status/events | read-only |
| Runtime | Interrupt | stop active work | elevated task control |
| Governance | Project Registry | track repositories, policies, stages and profiles | Controller-owned |
| Governance | Role Registry | map engineering roles to runtimes/agents/workspaces | Controller-owned |
| Governance | Task Contract | freeze scope, non-goals, acceptance and permissions | stage-bound |
| Governance | Stage Gate | admit/review/close engineering stages | Controller authority |
| Evidence | Validation | collect tests, lint, type, build and health results | mechanical only |
| Evidence | Diff correlation | bind evidence to exact repo/task/stage state | immutable reference |
| Repository | Branch/worktree | provision and bind workspaces to roles | policy-bound |
| Repository | Commit/push | automate mechanical Git actions | stage-bound |
| Repository | PR/CI | create/update PR and observe CI | policy-bound |
| Repository | Merge | execute only after valid state-bound authorization | Controller-authorized |
| Knowledge | Memory | retain decisions, failures, repairs and lessons | source of truth |
| Knowledge | Projection | render structured knowledge to Markdown | one-way by default |
| Knowledge | Obsidian | expose backlinks, human annotations and synthesis | human interface |
| Control Surface | CLI/MCP/API | offer typed structured operations | least authority |
| Audit | Event log | preserve task/stage/repository decision history | append-oriented |

---

## 2. Runtime capability contract

A runtime adapter advertises a capability profile rather than pretending every runtime behaves identically.

```yaml
runtime: codex
capabilities:
  discovery: true
  persistent_context: true
  structured_read: true
  resume: true
  dispatch: true
  live_status: true
  interrupt: true
  tool_events: true
```

```yaml
runtime: hermes
status: planned
capabilities: research_required
```

Möbius must route only operations supported by the selected runtime profile.

---

## 3. Role policy example

```yaml
role: backend
runtime: codex
workspace_strategy: dedicated_worktree
permissions:
  read_repo: true
  write_allowed_paths:
    - backend/**
  commit: true
  push: true
  open_pr: true
  merge: false
required_evidence:
  - tests
  - lint
  - typecheck
  - diff
```

```yaml
role: security-review
runtime: hermes
permissions:
  read_repo: true
  write_repo: false
  merge: false
required_output:
  - findings
  - severity
  - evidence_refs
```

---

## 4. Knowledge object model

```text
KnowledgeObject
├── ProjectMemory
├── ArchitectureDecision
├── StageRecord
├── FailureRecord
├── RepairPattern
├── EngineeringLesson
├── RuntimeFinding
├── ResearchThread
└── ValueThread
```

Each object should include:

```text
id
project
source_stage
source_task
source_repo_state
provenance
created_at
updated_at
summary
links
projection_state
```

---

## 5. Obsidian projection capabilities

Target projection functions:

```text
project_overview()
project_stage_record(stage_id)
architecture_decision(adr_id)
failure_fix_record(failure_id)
engineering_lesson(lesson_id)
research_thread(thread_id)
value_thread(thread_id)
refresh_backlinks()
```

Markdown projection should use stable IDs and frontmatter.

Example:

```yaml
---
mobius_id: stage:FlowTracer:BE-7
kind: stage_record
project: FlowTracer
status: closed
source_pr: 42
source_sha: abc123
provenance: mobius
---
```

---

## 6. Controller-facing commands

The ideal experience compresses implementation mechanics into high-level intent:

```text
Continue <project>
Show project state
Why is this stage blocked?
Review current evidence
Send fix back to backend
Approve reviewed state
Show all active agents
Show runtime health
Show what changed since last stage
Project latest lessons to Obsidian
```

Each natural-language action resolves to explicit typed operations and authority checks.

---

## 7. Automation boundary

### Automatically executable

- context packaging;
- task dispatch after admission;
- status observation;
- mechanical validation;
- evidence collection;
- branch/worktree preparation under policy;
- commit/push/PR mechanics under policy;
- CI observation;
- repair-task preparation after Controller FIX;
- knowledge extraction/projection after finalized stage.

### Explicit approval required

- architecture-changing decisions;
- stage admission when policy requires Controller decision;
- PASS/FIX/BLOCK judgment;
- merge authorization;
- release/production actions;
- destructive repository actions;
- bidirectional knowledge writes into authoritative structured state.

---

## 8. Product completeness test

Möbius reaches its intended mature form when one Controller can govern a real multi-agent project end-to-end without manually relaying routine information between agents, Git, CI and knowledge tools while still retaining explicit authority over consequential engineering decisions.

That means the system must prove all five outcomes:

1. **Execution** — agents can be addressed and controlled reliably.
2. **Governance** — engineering stages and permissions are explicit.
3. **Evidence** — claims are backed by correlated mechanical facts.
4. **Delivery** — Git/CI/PR mechanics are automated safely.
5. **Memory** — important project knowledge survives and becomes reusable through Möbius + Obsidian.
