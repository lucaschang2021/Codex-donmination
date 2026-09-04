# Möbius

**Architecture & Development Governance Control Plane for AI engineering.**

Möbius governs how Codex, Claude Code, Astra, Hermes, and future engineering runtimes plan, modify, validate, review, and evolve software systems without allowing implementation speed to silently destroy architecture, test contracts, or authority boundaries.

[简体中文](README.zh-CN.md) · [Master Architecture](docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md) · [Architecture Contract](docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md) · [Roadmap](ROADMAP.md) · [MIT](LICENSE)

> **Status:** pre-alpha / architecture-first. The current implementation path remains Codex-first, but Codex integration is now treated as the first governed execution runtime rather than the product definition.

## Why Möbius?

AI coding agents can already write code. The harder problem is governing continuous AI-driven software change:

- How do we stop a service from silently becoming a God module?
- How do we prevent transport adapters from turning into application kernels?
- How do we detect hidden dependencies, global mutable state, import-time side effects, and initialization-order coupling before they spread?
- How do we keep domain decisions out of orchestration layers?
- How do we preserve test isolation while adding providers, agents, frameworks, and integrations?
- How do we bind review and merge authority to exact repository state?

Möbius turns architectural intent into executable engineering governance.

> **Agents execute. Git records. Tests verify behavior. Architecture contracts constrain evolution. Evidence supports review. Möbius governs change.**

## Product thesis

Möbius is **not primarily a multi-agent orchestrator**.

Multi-agent execution is a pluggable strategy. The product core is governance over an engineering **Change**: its plan, architecture constraints, execution evidence, repository state, review, and final authority decision.

One governed Change may be executed by:

- one Codex session;
- Claude Code;
- Astra;
- Hermes;
- several engineering agents;
- a human developer;
- or a mixed workflow.

The same architecture contract applies regardless of who executes it.

## Six planes

| Plane | Responsibility |
|---|---|
| **Governance** | Controller authority, task/change contracts, stage gates, risk policy, PASS/FIX/BLOCK, exact-SHA merge authorization |
| **Architecture** | Architecture contracts, module responsibilities, dependency rules, side-effect policy, state ownership, complexity gates, architecture drift |
| **Runtime** | Codex first; Claude Code / Astra / Hermes and future runtimes behind normalized adapters |
| **Evidence** | diffs, tests, CI, dependency graph changes, architecture findings, validation manifests |
| **Repository** | branch/worktree lifecycle, commits, PRs, CI observation, reviewed-head binding, merge mechanics |
| **Knowledge** | ADRs, architecture-debt history, failures/fixes, engineering lessons, Obsidian-compatible projection |

```text
                         Human / Controller
                                  |
                                  v
+----------------------------------------------------------------+
|                             MÖBIUS                             |
|                                                                |
| Governance | Architecture | Runtime | Evidence | Repo | Memory |
+-------------+--------------+---------+----------+------+--------+
                |                |          |        |
                |                |          |        +--> Git / PR / CI
                |                |          +--> tests / diffs / architecture facts
                |                +--> Codex / Claude Code / Astra / Hermes
                +--> policy / stage gate / merge authority
```

## Architecture Contract

Each governed repository can declare a versioned Architecture Contract.

Example:

```yaml
schema_version: 1
project: FlowTracer

layers:
  api:
    may_depend_on: [application, schemas]
  application:
    may_depend_on: [domain, ports]
    forbidden: [fastapi, electron]
  domain:
    filesystem: forbidden
    network: forbidden
    environment_access: forbidden

mutable_state:
  module_globals: forbidden

required_checks:
  - unit_tests
  - contract_tests
  - architecture_gate
```

Möbius does not force one universal architecture. It enforces the architecture the project deliberately declares.

See [`docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md`](docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md).

## Architecture Gate

Before merge authorization, Möbius can evaluate architecture evidence such as:

- forbidden dependency directions;
- cross-layer imports;
- responsibility leakage;
- new global mutable state;
- import-time filesystem/network/plugin side effects;
- public-interface changes;
- architecture contract deviations;
- file/dependency complexity growth;
- loss of fake/in-memory test adapters;
- loss of failure isolation.

A passing test suite proves behavior under tests. It does **not** prove architecture integrity.

Example result:

```yaml
architecture_gate:
  status: FIX
  findings:
    - severity: P1
      rule: adapter_must_not_depend_on_entrypoint
      evidence: "REST adapter imports MCP entrypoint as business service"
      remediation: "extract an application service and inject it into both adapters"
```

## Governed development lifecycle

```text
REQUEST
  ↓
CONTEXT LOAD
  ↓
ARCHITECTURE CONTRACT SNAPSHOT
  ↓
PLAN
  ↓
PLAN GATE
  ↓
EXECUTION
  ↓
TEST / BUILD / CI EVIDENCE
  ↓
ARCHITECTURE DIFF
  ↓
INDEPENDENT REVIEW
  ↓
PASS / FIX / BLOCK
  ↓
MERGE AUTHORIZATION
  ↓
MERGE
  ↓
KNOWLEDGE EXTRACTION
```

The Plan Gate catches architectural mistakes before expensive execution. The Architecture Diff checks how the repository structure changed, not only which lines changed.

## Controller-first authority

Execution and authority are different things.

Mechanical work can be automated aggressively:

- repository inspection;
- worktree setup;
- dependency graph extraction;
- test/lint/type/build execution;
- architecture rule evaluation;
- evidence collection;
- PR metadata preparation;
- knowledge projection.

Architecture redefinition, security-risk acceptance, contract weakening, destructive migration approval, merge authorization, and release authority remain explicit policy/Controller decisions.

> **Automate evidence and mechanics. Preserve authority.**

## Runtime strategy

Möbius remains **Codex-first, not Codex-only**.

```text
EngineeringRuntime
├── CodexRuntime       # first implementation proof
├── ClaudeCodeRuntime  # planned
├── AstraRuntime       # planned
├── HermesRuntime      # planned
└── FutureRuntime
```

The Runtime Plane executes bounded Changes. It does not own architecture policy or merge authority.

The original persistent-Codex control bridge remains valuable and is preserved as the first implementation path.

## Repository governance

Git is a first-class subsystem rather than shell boilerplate delegated blindly to agents.

The target Repository Plane covers:

- repository inspection;
- branch/worktree lifecycle;
- role-to-workspace binding;
- commit/push;
- PR creation/update;
- CI observation;
- exact reviewed-head SHA binding;
- merge execution after authorization;
- post-merge synchronization.

A new commit invalidates prior exact-SHA merge authorization unless policy explicitly says otherwise.

## Knowledge memory

Möbius preserves:

- architecture decisions;
- Architecture Contract versions;
- stage/change records;
- architecture-debt findings;
- failures and fixes;
- runtime compatibility findings;
- engineering lessons;
- research and product threads.

Machine-readable Möbius state remains authoritative. Obsidian-compatible Markdown is a human projection, not a hidden control channel.

## Reference governance cases

### FinTerminal

Möbius should detect or prevent patterns such as:

- an HTTP adapter depending on an MCP entrypoint as a giant application kernel;
- import-time plugin registration;
- configuration/runtime state hidden in module globals;
- core logic requiring full-system initialization to test.

### FlowTracer

Möbius should preserve:

- bootstrap-only `main.py`;
- explicit dependency injection;
- fake provider implementations;
- clear service/provider boundaries;
- early warnings when acquisition/intelligence services trend toward God services.

### Gallop

Möbius should preserve:

- deterministic evidence/mastery/progression engines;
- event-journal authority;
- domain decisions outside orchestration services;
- Progressive Mentorship logic as dedicated deterministic engines rather than an ever-growing `Automation` class.

## Relationship to Rasputin

The products solve different governance problems:

```text
Rasputin
= runtime sovereign control, policy, authority, computational capital,
  verification/audit, inter-organization trust

Möbius
= development-time architecture and engineering-change governance
```

Möbius can later integrate with Rasputin, but it must remain independently useful to developers and repositories.

## Roadmap

| Phase | Target |
|---|---|
| **A — Contract MVP** | Architecture Contract schema, repository scanner, module/dependency map, baseline snapshot, initial Architecture Gate |
| **B — Codex governed execution** | persistent runtime discovery/read/dispatch/status + bounded Change contract + plan gate + evidence |
| **C — Architecture Diff** | dependency/state/side-effect/interface/complexity deltas and structured FIX/BLOCK findings |
| **D — Repository governance** | worktree/PR/CI/exact-SHA merge authorization |
| **E — Multi-runtime** | Claude Code / Astra / Hermes adapters and capability negotiation |
| **F — Knowledge** | ADR extraction, architecture-debt history, project memory, Obsidian projection |

See [`ROADMAP.md`](ROADMAP.md) for release sequencing.

## Documentation

- [`docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md`](docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md) — canonical product architecture
- [`docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md`](docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md) — executable architecture governance contract
- [`docs/00-PROJECT-CONTROL.md`](docs/00-PROJECT-CONTROL.md) — original Codex-first project-control baseline
- [`docs/02-R0-INTEGRATION-DECISION.md`](docs/02-R0-INTEGRATION-DECISION.md) — historical Codex integration decision
- [`docs/10-MASTER-TECHNICAL-DESIGN.md`](docs/10-MASTER-TECHNICAL-DESIGN.md) — original CodexRuntime implementation baseline

The Codex documents remain valid as implementation history unless a newer canonical document explicitly supersedes a product-level assumption.

## Permanent rules

1. Govern change, not intelligence.
2. Architecture is executable policy where possible.
3. Execution never implies authority.
4. Evidence never silently replaces judgment.
5. No runtime owns product architecture.
6. No transport adapter may become the application kernel.
7. Domain decisions belong in deterministic domain/application engines, not entrypoints.
8. Global mutable state requires an explicit owner and lifecycle.
9. Import-time side effects are exceptional and declared.
10. Architecture drift must be observable before it becomes architecture collapse.
11. Contract changes are versioned and reviewable.
12. Möbius must eventually govern its own repository using the same rules it offers to others.

## License

Möbius is licensed under the [MIT License](LICENSE).
