# Möbius Architecture Gate Specification v1

> Status: **Normative MVP specification**

The Architecture Gate is the first implementation target that makes Möbius more than an orchestration wrapper. It turns architectural intent into reviewable, partially executable policy.

## 1. Inputs

The gate consumes:

- repository snapshot before change;
- repository snapshot after change;
- Architecture Contract;
- Change Contract;
- implementation plan;
- Git diff and file metadata;
- test / lint / type / build evidence;
- optional runtime and CI evidence.

## 2. Required checks

### AG-DEP — Dependency direction

Detect:

- forbidden cross-layer imports;
- adapter-to-adapter coupling;
- domain/application depending on framework or transport internals;
- direct infrastructure access that bypasses declared ports/services;
- newly introduced circular dependencies.

### AG-RESP — Module responsibility

Detect:

- modules absorbing responsibilities outside their declared contract;
- orchestration modules accumulating domain decision rules;
- entrypoints becoming application kernels;
- repeated forwarding through a giant facade instead of shared services.

### AG-STATE — State ownership

Detect:

- new mutable module globals;
- hidden singleton state;
- state shared without explicit lifecycle owner;
- cache/session/config state introduced outside declared owner.

### AG-SIDE — Side-effect policy

Detect import-time or hidden:

- filesystem writes;
- network calls;
- plugin registration;
- process/thread startup;
- environment mutation;
- database/Redis/provider connection attempts.

### AG-DI — Dependency visibility

Detect core code that reaches directly into:

- environment variables;
- global config;
- model/API clients;
- clocks/randomness;
- persistence sessions;
- network providers;

when the contract requires explicit injection or ports.

### AG-CPLX — Complexity growth

Track soft/hard budgets for:

- file length;
- outgoing dependency count;
- cyclomatic/cognitive complexity when available;
- number of public responsibilities;
- module fan-in/fan-out;
- rate of growth across changes.

Soft thresholds warn; hard thresholds block only when the project contract says so.

### AG-API — Contract/interface change

Detect:

- public API/schema changes;
- event/persistence format changes;
- migrations;
- breaking adapter contracts;
- unversioned semantic reinterpretation.

### AG-TEST — Isolation and validation

Check whether:

- changed core modules still have isolated tests;
- fake/in-memory providers can replace external services when required;
- architecture contract tests run;
- changed policy paths have rejection/failure tests;
- behavior tests remain green.

## 3. Severity model

| Severity | Meaning | Default disposition |
|---|---|---|
| P0 | Catastrophic authority/security/data-integrity violation | BLOCK |
| P1 | Strong architecture-contract violation likely to create structural debt | FIX/BLOCK |
| P2 | Significant drift or complexity risk | FIX or explicit accept |
| P3 | Soft-budget warning / maintainability signal | PASS with warning |

## 4. Gate output

```yaml
architecture_gate:
  schema_version: mobius.architecture-gate/v1
  change_id: CHG-123
  status: FIX
  summary:
    p0: 0
    p1: 1
    p2: 1
    p3: 0
  findings:
    - id: AG-DEP-001
      severity: P1
      rule: adapter_to_adapter_dependency_forbidden
      location: api_server.py
      evidence: REST adapter imports MCP entrypoint
      remediation: extract shared application service
    - id: AG-CPLX-004
      severity: P2
      rule: service_soft_budget_exceeded
      location: acquisition.py
      evidence: module responsibility/dependency growth exceeded baseline
      remediation: split orchestration responsibilities before further expansion
```

## 5. Plan Gate vs Post-change Gate

Möbius uses two related checks.

### Plan Gate

Runs before write execution. It asks:

- Is the proposed implementation path architecturally admissible?
- Are the correct modules targeted?
- Is a migration/ADR/exception required first?

### Post-change Architecture Gate

Runs after implementation. It asks:

- Did the actual code preserve the admitted architecture?
- What changed in dependency/state/side-effect/interface structure?
- Is the implementation eligible for review/merge?

A PASS at Plan Gate does not guarantee a PASS after implementation.

## 6. Baseline and drift

The gate should maintain a project architecture baseline so that it can distinguish:

- pre-existing debt;
- newly introduced debt;
- debt reduced by the current change;
- explicitly accepted exceptions.

Möbius should not block every change merely because a legacy repository already contains violations. Default policy for legacy systems is **no-regression + targeted reduction**.

## 7. Legacy-system strategy

For repositories such as FinTerminal, governance should support strangler refactoring:

```text
baseline existing debt
-> forbid new violations
-> identify extraction seams
-> introduce shared application services/ports
-> move adapters off giant kernel
-> eliminate hidden state/side effects incrementally
```

The gate must therefore report both:

- `existing_findings`;
- `introduced_findings`;
- `resolved_findings`.

## 8. Reference project policies

### FinTerminal

High-priority checks:

- adapter-to-adapter imports;
- giant application kernel;
- import-time plugin/config/filesystem behavior;
- global model/session/config state;
- core testability without MCP/FastAPI/provider/keyring.

### FlowTracer

High-priority checks:

- keep `create_app` as composition/bootstrap;
- protect typed settings/provider abstractions;
- prevent acquisition/intelligence services from becoming God services;
- preserve fake-provider testability;
- warn on ORM/application boundary expansion where contract forbids it.

### Gallop

High-priority checks:

- deterministic domain/policy engines remain side-effect free;
- `Automation` remains orchestration rather than mentorship-decision owner;
- event journal remains authority for Automation state;
- Progressive Mentorship components are independently testable;
- external adapters cannot promote mastery by themselves.

## 9. MVP implementation order

1. Contract parser + validation.
2. Python import graph scanner.
3. Module/file responsibility map.
4. Mutable-global scan.
5. Import-time side-effect heuristics.
6. Complexity/file-growth baseline.
7. Git before/after architecture diff.
8. Structured gate report.
9. CI/PR integration.
10. Runtime-aware Plan Gate.

The first MVP should prefer explainable deterministic checks over LLM-only judgment. Models may assist classification and recommendations, but the evidence and rule being evaluated must remain explicit.
