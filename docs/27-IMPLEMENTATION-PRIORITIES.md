# Möbius Implementation Priorities

> Status: **Execution order after architecture reset**

The architecture reset does not authorize broad implementation. The first releases should prove the governance thesis with deterministic tooling before adding broad multi-runtime orchestration.

## P0 — Architecture Contract MVP

### Implemented baseline

The self-governed repository baseline now proves an initial slice:

- TOML Architecture Contract loading;
- explicit domain / ports / application / infrastructure / adapters / bootstrap boundaries;
- static Python AST repository scanning without importing target code;
- import collection;
- mutable module-global detection for list/dict/set literals;
- direct top-level call detection;
- file line-count evidence;
- deterministic dependency/state/side-effect/complexity rule evaluation;
- structured PASS/FIX/BLOCK report;
- thin CLI;
- dependency injection through ports and a single composition root;
- isolated tests;
- CI self Architecture Gate.

This is an implementation baseline, not P0 completion.

### Remaining P0 work

1. explicit contract schema/type validation with deterministic configuration errors;
2. repository/module graph model rather than a flat import list;
3. architecture baseline snapshot persistence/serialization;
4. richer dependency resolution, including relative imports and package ownership;
5. rule provenance and stable finding identifiers;
6. baseline-no-regression classification for legacy repositories;
7. reference-project fixtures/policies for FinTerminal, FlowTracer, and Gallop;
8. reproducible acceptance runs against those three repositories.

P0 exits only when those acceptance runs reproduce the known architecture findings and preservation rules without executing target application code.

## P1 — Architecture Diff

Add before/after comparison for:

- dependency edges;
- mutable globals;
- import-time side effects;
- module/file growth;
- public interfaces;
- test isolation signals.

Legacy repositories must support `existing / introduced / resolved` finding classes.

## P2 — Governed Codex execution

Reuse the existing Codex integration work, but bind dispatch to a governed Change:

```text
Change Contract
-> Plan Gate
-> CodexRuntime
-> execution evidence
-> Architecture Diff
-> review
```

The previous persistent-thread work remains useful here.

## P3 — Repository governance

Add worktrees, PRs, CI observation, exact-SHA authorization, and controlled merge mechanics.

## P4 — Multi-runtime

Only after P0–P3 are stable:

- Claude Code;
- Astra;
- Hermes;
- future runtimes.

## P5 — Knowledge projection

Add ADR/debt/history extraction and Obsidian projection after authoritative machine state is stable.

## Explicit non-priority

Do not prioritize early:

- graphical dashboard;
- large autonomous swarm;
- generic model router;
- autonomous release authority;
- broad project-management suite.

The first product proof is simple:

> Möbius can detect and prevent architecture drift in real AI-engineered repositories while allowing agents to keep shipping changes quickly.
