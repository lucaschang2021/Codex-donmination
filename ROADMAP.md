# Möbius Roadmap

Möbius is being developed as an **Architecture & Development Governance Control Plane for AI engineering**.

The original Codex control bridge remains the first execution proof, but the roadmap is now organized around governed software change rather than persistent-thread control alone.

## Phase A — Architecture Contract MVP

Goal: make architectural intent machine-readable and reviewable before adding broad runtime orchestration.

Required capabilities:

- versioned Architecture Contract schema;
- repository/module discovery;
- import/dependency graph extraction;
- module responsibility map;
- explicit side-effect and mutable-state policy;
- baseline architecture snapshot;
- deterministic Architecture Gate report;
- PASS / FIX / BLOCK result with reproducible evidence.

Definition of done:

A real repository can declare architectural rules and Möbius can detect at least:

- one forbidden dependency direction;
- one import-time side effect or unmanaged global state pattern;
- one complexity-growth warning;
- one test-isolation regression or missing fake-provider boundary.

## Phase B — Codex Governed Execution

Goal: preserve the original Codex-first control-loop work while placing it under a Change contract.

Required capabilities:

- discover persistent Codex threads;
- read structured context;
- dispatch one bounded Change;
- observe execution status;
- bind task execution to a repository/branch/worktree;
- snapshot the Architecture Contract before execution;
- capture implementation evidence;
- run a Plan Gate before dispatch.

Definition of done:

```text
Controller
  -> selects repository + Change objective
  -> Möbius loads architecture contract
  -> validates plan
  -> targets CodexRuntime
  -> dispatches bounded task
  -> watches execution
  -> collects changed-file/test evidence
  -> produces architecture diff
  -> returns PASS / FIX / BLOCK for Controller review
```

## Phase C — Architecture Diff

Goal: reason about how repository structure changed, not only which lines changed.

Planned evidence:

- dependency graph delta;
- new/removed module edges;
- cross-layer import changes;
- interface changes;
- new environment/filesystem/network/subprocess side effects;
- mutable-state ownership changes;
- file/module complexity delta;
- new framework coupling;
- loss of isolated unit-testability;
- failure-isolation regressions.

The Architecture Diff must separate:

- observed facts;
- policy violations;
- advisory warnings;
- final authority decisions.

## Phase D — Repository Governance

Goal: make Git and PR state first-class governed objects.

Planned capabilities:

- branch/worktree lifecycle;
- role/runtime-to-workspace binding;
- commit/push;
- PR creation/update;
- CI observation;
- reviewed-head SHA binding;
- merge authorization;
- authorization invalidation when the reviewed head changes;
- post-merge synchronization.

Mechanical Git actions may be automated. Merge/release authority must remain explicit policy/Controller decisions.

## Phase E — Multi-runtime Expansion

Goal: prove that the governance model is runtime-independent.

Planned adapters:

- Claude Code;
- Astra;
- Hermes;
- future engineering runtimes.

Required design:

```text
EngineeringRuntime
  discover()
  read_context()
  dispatch(change_contract)
  observe()
  interrupt()
  collect_result()
  capabilities()
```

Multi-agent orchestration remains a pluggable execution strategy, not the product definition.

## Phase F — Knowledge & Architecture Memory

Goal: retain engineering knowledge without making human notes the hidden source of truth.

Planned capabilities:

- ADR extraction;
- Architecture Contract history;
- architecture-debt ledger;
- repeated failure-pattern memory;
- runtime compatibility findings;
- project/stage/change records;
- Obsidian-compatible one-way projection.

Any future bidirectional knowledge mode requires explicit provenance and conflict-resolution rules.

## Reference-project hardening

Möbius development should continuously test governance against real project patterns.

### FinTerminal

Target detections:

- adapter -> entrypoint/business-kernel coupling;
- import-time plugin loading;
- module-global runtime state;
- hidden initialization-order requirements;
- core logic that cannot be isolated from transport/runtime startup.

### FlowTracer

Target preservation rules:

- bootstrap-only application entrypoint;
- explicit dependency injection;
- provider abstraction and fake providers;
- service boundary integrity;
- early warning for acquisition/intelligence God-service growth.

### Gallop

Target preservation rules:

- deterministic evidence/progression engines;
- event-journal authority;
- orchestration service remains orchestration-only;
- Progressive Mentorship logic stays in dedicated deterministic modules;
- provider output never directly becomes mastery authority.

## Version sequence

The exact version numbers may change as implementation evidence arrives, but the intended sequence is:

| Version | Primary proof |
|---|---|
| **v0.1** | Architecture Contract + repository scanner + baseline Architecture Gate |
| **v0.2** | Codex governed Change loop |
| **v0.3** | Architecture Diff + structured findings |
| **v0.4** | Repository/worktree/PR governance |
| **v0.5** | CI + exact-SHA review/merge authorization |
| **v0.6** | Multi-runtime adapter boundary |
| **v0.7** | Claude Code / Astra / Hermes experiments |
| **v0.8** | Architecture memory / ADR / debt ledger |
| **v0.9** | MCP/API control surface for external controllers |
| **v1.0** | Stable architecture-governed AI engineering control plane |

## Non-goals for early versions

Early versions MUST NOT become:

- a generic autonomous software factory;
- a benchmark for which model is “smartest”;
- an unrestricted agent swarm;
- a replacement for Git, CI, test frameworks, or IDEs;
- an automatic authority system that silently weakens architecture or security rules;
- a universal clean-architecture enforcer.

Möbius governs the architecture a project deliberately declares.

## Design rule

> **Govern change, not intelligence. Automate evidence and mechanics. Preserve architecture, judgment, review, and explicit authority.**
