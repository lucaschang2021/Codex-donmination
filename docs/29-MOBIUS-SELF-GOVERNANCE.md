# Möbius Self-Governance Baseline

> Status: **Normative engineering baseline for the Möbius repository**

Möbius must obey the architecture-governance rules it expects other repositories to adopt. This document defines the repository-level engineering baseline used to keep that promise.

## 1. Source of truth hierarchy

When documents or examples disagree, use this order:

1. `ARCHITECTURE.toml` — machine-readable repository architecture contract;
2. `docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md` — product architecture;
3. `docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md` — generic contract semantics;
4. `docs/23-ARCHITECTURE-GATE-SPEC.md` — gate semantics;
5. stage/implementation notes;
6. historical `Codex Domination` documents.

Historical documents remain useful evidence but do not override the current canonical product or repository architecture.

## 2. Repository architecture

```text
src/mobius/
  domain/          deterministic governance models and rules
  ports/           abstract boundaries owned by core/application
  application/     use-case orchestration only
  infrastructure/  filesystem, Git, provider and runtime implementations
  adapters/        CLI/API/MCP transport translation only
  bootstrap.py     single composition root

tests/             isolated unit and contract tests
ARCHITECTURE.toml   executable repository architecture policy
```

## 3. Permanent engineering rules

1. Domain logic is side-effect free.
2. Application services depend on ports, never concrete infrastructure.
3. Adapters do not become application kernels.
4. Concrete dependencies are assembled only in bootstrap/composition roots.
5. Mutable runtime state has an explicit owner and lifecycle.
6. Import-time network/filesystem/process/plugin mutation is prohibited unless explicitly declared.
7. Core behavior must remain testable through fakes/in-memory implementations.
8. Static inspection must not import or execute target repository code.
9. Passing tests and passing architecture gates are separate evidence classes.
10. Contract changes are explicit, versioned, and independently reviewable.
11. Existing legacy debt is baselined; new regressions are blocked.
12. Möbius should be able to run its own Architecture Gate in CI.

## 4. Self-gate lifecycle

Every non-trivial change should pass:

```text
PLAN
  -> contract check
  -> implementation
  -> unit/type/lint evidence
  -> Mobius Architecture Gate
  -> review
  -> merge authorization
```

As Architecture Diff matures, CI should evolve from a single snapshot gate to baseline-vs-candidate classification:

```text
existing / introduced / resolved
```

An existing P2/P3 debt item may be tracked without blocking unrelated work. An introduced P0/P1 violation blocks merge.

## 5. Runtime and provider adapters

Codex, Claude Code, Astra, Hermes, GitHub, Git, CI, Obsidian, and other external systems are integrations, not domain dependencies.

Each integration should eventually implement an explicit port and must provide:

- deterministic error semantics;
- capability declaration where relevant;
- fake/test implementation when practical;
- explicit lifecycle ownership;
- no import-time connection or registration;
- failure isolation from unrelated capabilities.

## 6. God-module prevention

Soft warning thresholds live in `ARCHITECTURE.toml`. File size alone is not sufficient evidence, so later gates should also monitor:

- import fan-in/fan-out;
- number of owned mutable states;
- number of external systems known by one module;
- number of distinct responsibilities;
- public interface growth;
- test fixture breadth;
- frequency of unrelated edits to the same module.

A growing application service should be decomposed by responsibility before it becomes the equivalent of FinTerminal's historical giant application kernel.

## 7. Reference lessons encoded in Möbius

### From FinTerminal

Avoid adapter-to-entrypoint business coupling, module-global runtime state, import-time plugin/config side effects, and cores that require full-system startup.

### From FlowTracer

Preserve explicit bootstrap, typed configuration boundaries, provider abstractions, fake providers, service decomposition, and lifecycle-managed infrastructure.

### From Gallop

Keep deterministic domain rules separate from orchestration, retain explicit evidence authority, and prevent feature growth from turning an application service into a God service.

## 8. Current implementation truth

The repository is still pre-alpha. The initial code baseline proves only a narrow slice:

- Architecture Contract loading;
- static Python scanning;
- deterministic dependency/state/side-effect/complexity findings;
- thin CLI;
- dependency injection through ports and bootstrap;
- isolated tests;
- CI self-gate.

It does **not** yet claim full Architecture Diff, Git/PR governance, multi-runtime orchestration, merge authorization, knowledge projection, or production readiness.

## 9. Definition of repository health

Möbius is healthy when:

- the core can be imported/tested without external services;
- target repositories can be scanned without executing them;
- dependency direction is machine-checkable;
- no hidden global runtime state is required;
- CI reproduces the architecture gate;
- architecture exceptions are visible rather than silently normalized;
- documentation clearly distinguishes current implementation from target architecture.
