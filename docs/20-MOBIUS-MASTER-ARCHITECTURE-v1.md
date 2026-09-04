# Möbius Master Architecture v1

> **Status:** Canonical product architecture
>
> Möbius is an **Architecture & Development Governance Control Plane for AI engineering**. It governs how heterogeneous coding agents plan, modify, validate, review, and evolve software systems without allowing implementation speed to silently destroy architecture, test contracts, or authority boundaries.

## 1. Product thesis

Frontier coding agents can already write software. The emerging systems problem is different:

> How do we let Codex, Claude Code, Astra, Hermes, and future engineering agents modify complex repositories continuously while preserving architectural integrity, explicit authority, reproducibility, and evidence?

Möbius answers that problem.

It is **not primarily a multi-agent orchestrator**. Multi-agent execution is one pluggable execution strategy. The product core is governance over engineering change.

```text
Agents execute.
Git records.
Tests verify behavior.
Architecture contracts constrain evolution.
Evidence supports review.
Möbius governs change.
```

## 2. Core governed object: Change

Möbius treats an engineering change as the primary governed object.

A Change includes:

- objective and non-goals;
- target repository / branch / worktree;
- owning role and runtime;
- architecture contract snapshot;
- allowed and forbidden dependency directions;
- allowed files / modules / capabilities;
- implementation plan;
- execution evidence;
- architecture diff;
- test / CI / build evidence;
- review findings;
- final authority decision.

This is intentionally broader than an agent task. One change may be executed by one agent, several agents, a human, or a mixed workflow.

## 3. Six planes

### 3.1 Governance Plane

Owns authority, policy, stage gates, task admission, review requirements, risk classification, and merge authorization.

Responsibilities:

- Controller authority;
- role registry;
- change contracts;
- stage admission;
- PASS / FIX / BLOCK decisions;
- risk policy;
- exact-SHA merge authorization.

### 3.2 Architecture Plane

Owns architectural truth and machine-checkable constraints.

Responsibilities:

- architecture contracts;
- module responsibility map;
- dependency direction rules;
- forbidden cross-layer imports;
- state ownership;
- side-effect policy;
- configuration ownership;
- interface / port boundaries;
- complexity and file-growth thresholds;
- architecture decision records;
- architecture drift detection.

### 3.3 Runtime Plane

Normalizes heterogeneous engineering runtimes.

```text
EngineeringRuntime
├── CodexRuntime
├── ClaudeCodeRuntime
├── AstraRuntime
├── HermesRuntime
└── FutureRuntime
```

The runtime plane performs execution; it does not own architecture or merge authority.

### 3.4 Evidence Plane

Collects machine-verifiable evidence:

- changed files;
- diff metadata;
- dependency graph changes;
- test results;
- coverage;
- lint / type checks;
- build results;
- migration checks;
- runtime failures;
- CI facts;
- contract deviations;
- architecture gate findings.

### 3.5 Repository Plane

Owns Git mechanics and exact repository state:

- branch / worktree lifecycle;
- commit / push;
- PR creation and update;
- CI observation;
- reviewed-head binding;
- merge execution after authorization;
- post-merge synchronization.

### 3.6 Knowledge Plane

Retains architecture decisions, engineering lessons, failure patterns, runtime compatibility findings, project history, and human-readable projections such as Obsidian Markdown.

Knowledge is not allowed to override machine-readable project state silently.

## 4. Architecture Contract

Every governed repository may define a versioned Architecture Contract.

Example:

```yaml
schema_version: 1
project: FlowTracer

layers:
  api:
    may_depend_on: [application, schemas]
    forbidden: [infrastructure_internal]
  application:
    may_depend_on: [domain, ports]
    forbidden: [fastapi, electron]
  domain:
    side_effects: forbidden
    filesystem: forbidden
    network: forbidden
    environment_access: forbidden

state_ownership:
  database_session: infrastructure
  application_config: bootstrap

complexity:
  max_file_lines_soft: 500
  max_new_dependencies_soft: 8

required_checks:
  - unit_tests
  - contract_tests
  - architecture_gate
```

Contracts are policy inputs, not universal style dogma. A repository may intentionally choose a modular monolith, event-sourced core, service architecture, ports-and-adapters model, or another design. Möbius enforces the declared architecture rather than forcing one architecture on every project.

## 5. Architecture Gate

A Change passes through an Architecture Gate before merge authorization.

The gate evaluates at minimum:

1. **Dependency direction** — did a lower-level module begin depending on an adapter or framework layer?
2. **Module responsibility** — did orchestration absorb domain decision logic?
3. **Hidden dependencies** — did new environment, filesystem, global-state, singleton, or initialization-order requirements appear?
4. **Import safety** — do imports now perform network, filesystem mutation, plugin registration, process startup, or other uncontrolled side effects?
5. **State ownership** — was mutable state placed in a module namespace or shared without an explicit owner?
6. **Interface stability** — were public contracts changed without versioning or migration?
7. **Complexity growth** — is a service or module trending toward a God module?
8. **Test isolation** — can the changed core still be tested with fake/in-memory adapters?
9. **Failure isolation** — can one provider/runtime failure be contained?
10. **Architecture intent** — does the implementation still match the accepted plan / ADR?

The output is structured evidence, for example:

```yaml
architecture_gate:
  status: FIX
  findings:
    - id: AG-DEP-001
      severity: P1
      file: api_server.py
      rule: adapter_must_not_depend_on_entrypoint
      evidence: "REST adapter imports MCP entrypoint module"
      recommendation: "extract application service and inject it into both adapters"
```

## 6. Governed development lifecycle

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

### Plan Gate

Before execution, Möbius checks that the proposed plan:

- targets the correct modules;
- respects declared boundaries;
- identifies migrations / compatibility concerns;
- has explicit acceptance criteria;
- does not silently broaden scope.

### Architecture Diff

After execution, Möbius compares architectural state before and after the change rather than reviewing only text diffs.

Potential derived artifacts:

- import/dependency graph delta;
- new global state;
- new side effects;
- module-size / complexity delta;
- interface delta;
- architecture contract violations;
- test isolation regressions.

## 7. Multi-agent execution is subordinate to governance

Möbius can route a change to multiple engineering roles, but orchestration is not the moat.

```text
                  Möbius Governance
                         |
              +----------+----------+
              |                     |
        Architecture Gate      Evidence Gate
              |                     |
              +----------+----------+
                         |
                  Execution Strategy
                         |
          +--------------+--------------+
          |              |              |
        Codex        Claude Code       Astra
```

A single-agent workflow and a multi-agent workflow are governed by the same Change contract.

## 8. Controller and automation authority

Möbius separates mechanical automation from authority.

Safe to automate aggressively:

- repository inspection;
- dependency graph extraction;
- worktree setup;
- test / lint / type / build execution;
- architecture rule evaluation;
- evidence collection;
- PR metadata preparation;
- knowledge projection.

Requires explicit policy or Controller authority:

- architecture redefinition;
- security-risk acceptance;
- contract weakening;
- destructive migration approval;
- merge authorization;
- release authority.

## 9. Relationship to the wider stack

Möbius has a narrow relationship with neighboring projects:

- **Rasputin** — runtime sovereign control, policy, authority, computational capital, verification, audit, and inter-organization trust for AI execution.
- **Möbius** — development-time architecture and engineering-change governance.
- **FlowTracer** — acquisition / monitoring / information intake product; also a reference repository for Möbius governance.
- **Gallop** — learning orchestration system; its deterministic domain core and service boundaries are a reference architecture-governance case.
- **FinTerminal** — financial vertical application and an important architecture-debt remediation case for Möbius.

Möbius may integrate with Rasputin later, but it must remain usable as an independent developer tool.

## 10. Reference governance cases

### FinTerminal

Detect and prevent:

- REST adapter depending on MCP entrypoint as a giant application kernel;
- import-time plugin loading;
- configuration and mutable state hidden in module globals;
- core logic requiring full-system initialization.

### FlowTracer

Protect:

- clean bootstrap and dependency injection;
- provider abstraction;
- test fakes;
- service/module boundaries;
- early warning when acquisition/intelligence services grow into God services.

### Gallop

Protect:

- deterministic evidence reducer;
- event journal authority;
- domain rules outside orchestration service;
- Progressive Mentorship logic as dedicated deterministic engines rather than methods accumulating in `Automation`.

## 11. Implementation strategy

Möbius remains architecture-first but implementation must proceed narrowly.

### Phase A — Architecture Contract MVP

- repository scanner;
- contract schema;
- module map;
- import/dependency graph;
- baseline architecture snapshot;
- initial architecture gate report.

### Phase B — Codex governed execution

- persistent runtime discovery/read/dispatch/status;
- bounded Change contract;
- execution evidence;
- plan gate;
- post-change architecture diff.

### Phase C — Repository governance

- branch/worktree lifecycle;
- PR integration;
- CI evidence;
- exact-SHA review binding;
- merge authorization.

### Phase D — Multi-runtime

- Claude Code / Astra / Hermes adapters;
- capability negotiation;
- normalized runtime evidence.

### Phase E — Knowledge and organization memory

- ADR extraction;
- architecture-debt history;
- project lessons;
- Obsidian-compatible projection.

## 12. Permanent design rules

1. **Govern change, not intelligence.**
2. **Architecture is executable policy where possible.**
3. **Execution never implies authority.**
4. **Evidence never silently replaces judgment.**
5. **No runtime owns the product architecture.**
6. **No adapter may become the application kernel.**
7. **Domain decisions belong in deterministic domain/application engines, not transport entrypoints.**
8. **Global mutable state requires an explicit owner and lifecycle.**
9. **Import-time side effects are exceptional and must be declared.**
10. **Architecture contracts are versioned and reviewable.**
11. **Architecture drift must be observable before it becomes architecture collapse.**
12. **Möbius must govern its own repository with the same rules it offers to others.**
