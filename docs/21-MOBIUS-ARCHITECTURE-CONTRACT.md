# Möbius Architecture Contract v1

> **Status:** Normative governance contract
>
> This document defines the minimum machine-readable contract Möbius uses to govern repository architecture. It is intentionally repository-agnostic.

## 1. Purpose

An Architecture Contract translates architectural intent into reviewable policy.

It answers:

- Which modules exist and what are they responsible for?
- Which dependency directions are allowed?
- Which cross-layer imports are forbidden?
- Where may mutable state live?
- Where may environment, filesystem, network, subprocess, database, or runtime side effects occur?
- Which interfaces are stable?
- Which tests and architecture checks are required before a change is admitted?
- Which architecture changes require an ADR or Controller approval?

The contract is not a style guide. It is a **change-governance boundary**.

## 2. Contract lifecycle

```text
DEFINE
  ↓
VERSION
  ↓
BASELINE SNAPSHOT
  ↓
CHANGE PLAN
  ↓
PRE-EXECUTION CHECK
  ↓
EXECUTION
  ↓
POST-CHANGE ARCHITECTURE DIFF
  ↓
PASS / FIX / BLOCK
  ↓
OPTIONAL CONTRACT REVISION VIA ADR
```

Implementation is never allowed to silently redefine the contract.

## 3. Minimal schema

```yaml
schema_version: 1
project: example-project
architecture_version: 1

modules:
  api:
    responsibility: transport_adapter
  application:
    responsibility: orchestration
  domain:
    responsibility: deterministic_domain_logic
  infrastructure:
    responsibility: external_io

rules:
  dependencies:
    api:
      may_depend_on: [application, schemas]
      forbidden: [infrastructure_internal]
    application:
      may_depend_on: [domain, ports]
    domain:
      forbidden: [api, infrastructure, framework]

  side_effects:
    domain:
      filesystem: forbidden
      network: forbidden
      subprocess: forbidden
      environment: forbidden
    infrastructure:
      filesystem: allowed
      network: allowed

  mutable_state:
    module_globals: forbidden
    explicit_owners:
      app_config: bootstrap
      database_session: infrastructure

  imports:
    import_time_side_effects: forbidden

  complexity:
    max_file_lines_soft: 500
    max_file_lines_hard: 900
    max_outgoing_module_dependencies_soft: 10

  tests:
    core_requires_isolated_unit_tests: true
    fake_external_providers_required: true
    architecture_gate_required: true
```

## 4. Rule classes

### AC-DEP — Dependency direction

Detects forbidden architectural edges.

Examples:

- domain -> FastAPI;
- application -> Electron renderer;
- HTTP adapter -> MCP entrypoint used as business kernel;
- lower-level service -> UI layer.

### AC-RESP — Module responsibility

Detects responsibility leakage.

Examples:

- orchestration service begins implementing domain scoring rules;
- API handler performs persistence and domain decisions directly;
- runtime adapter owns merge policy.

### AC-STATE — State ownership

Detects unmanaged mutable state.

Examples:

- module-level mutable list/dict used across requests;
- global current session without lifecycle owner;
- hidden singleton with cross-test contamination.

### AC-SIDE — Side-effect policy

Detects side effects in disallowed layers or at import time.

Examples:

- importing a module loads plugins;
- importing config writes directories;
- domain import reads environment variables;
- utility import starts subprocesses.

### AC-INT — Interface stability

Detects public contract changes.

Examples:

- renamed public API without migration;
- changed event schema without version bump;
- altered persistence format without migration design.

### AC-CPLX — Complexity growth

Detects emerging God modules and dependency hubs.

Signals may include:

- file-size growth;
- function/class growth;
- import fan-in/fan-out;
- number of responsibilities;
- number of mutable states owned;
- number of infrastructure integrations known by one module.

### AC-TEST — Isolation and testability

Detects loss of independently testable core logic.

Examples:

- core tests now require real Redis;
- business rules require full FastAPI startup;
- provider interface loses fake/in-memory implementation;
- unit test becomes end-to-end-only after a change.

### AC-FAIL — Failure isolation

Detects architecture where one external dependency can unnecessarily break unrelated capabilities.

## 5. Severity model

```text
P0 — architecture/security integrity failure; block immediately
P1 — major boundary violation or strong long-term coupling risk; FIX before merge
P2 — meaningful architecture debt; explicit acceptance required
P3 — advisory improvement
```

A repository may override severity for specific rules, but weakening a P0/P1 baseline requires an ADR.

## 6. Architecture Gate output

```yaml
change_id: chg-2026-00142
architecture_contract_version: 1
baseline_sha: abc123
candidate_sha: def456
status: FIX

summary:
  violations: 2
  warnings: 1

findings:
  - id: AC-DEP-001
    severity: P1
    path: src/api/server.py
    evidence: "imports src.runtime.entrypoint as business service"
    expected: "transport adapters depend on application services"
    remediation: "extract ResearchService and inject it into API and runtime adapters"

  - id: AC-SIDE-004
    severity: P1
    path: src/plugins.py
    evidence: "plugin registry mutates during module import"
    remediation: "move plugin registration to explicit bootstrap lifecycle"
```

## 7. Architecture Contract vs ADR

The contract defines current architectural law.

An ADR explains a deliberate architectural change.

```text
Implementation disagrees with contract
            |
            +--> implementation defect -> FIX
            |
            +--> contract is wrong -> ADR + Controller approval -> new contract version
```

The implementation itself is never evidence that the contract should change.

## 8. Plan Gate

Before dispatching work, Möbius evaluates the proposed plan against the contract.

The plan should declare:

- target modules;
- expected new dependencies;
- interfaces touched;
- state changes;
- persistence changes;
- migrations;
- tests to add/change;
- architecture exceptions requested.

If the plan already violates the architecture, Möbius should stop before expensive agent execution begins.

## 9. PR Governance

For a pull request, Möbius should attach four classes of evidence:

1. **Behavior evidence** — tests, lint, type checks, builds, CI.
2. **Repository evidence** — exact head SHA, changed files, migrations, generated artifacts.
3. **Architecture evidence** — dependency graph diff, side-effect diff, state ownership diff, interface diff, complexity diff.
4. **Authority evidence** — reviewer/controller decision bound to exact SHA.

A new commit invalidates prior exact-SHA merge authorization unless policy explicitly states otherwise.

## 10. Reference project policies

### FinTerminal

Recommended hard rules:

- HTTP/MCP adapters may not depend on each other;
- entrypoint modules may not expose business services;
- plugin loading must occur in bootstrap, not import time;
- mutable module globals prohibited for runtime state;
- core analysis logic must be testable without MCP/FastAPI/Electron.

### FlowTracer

Recommended rules:

- `main.py` remains bootstrap-only;
- provider interfaces retain fake test implementations;
- services may not absorb transport concerns;
- `acquisition.py` and `intelligence.py` receive complexity growth gates;
- infrastructure initialization stays in explicit lifecycle code.

### Gallop

Recommended rules:

- deterministic mastery/progression rules remain side-effect free;
- `automation/service.py` remains orchestration-only;
- Progressive Mentorship decisions live in dedicated deterministic engines;
- event journal remains authoritative over derived projections;
- provider output never directly promotes mastery.

## 11. Permanent constraints

1. Contract changes are versioned.
2. Architecture exceptions are explicit.
3. An agent cannot waive a violation it introduced.
4. A passing test suite does not override architecture policy.
5. An architecture gate cannot claim behavioral correctness.
6. Architecture evidence must be reproducible from repository state where possible.
7. Möbius must separate facts, policy evaluation, and final authority decisions.
