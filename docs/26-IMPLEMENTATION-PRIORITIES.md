# Möbius Implementation Priorities

> Status: **Execution order after architecture reset**

The architecture reset does not authorize broad implementation. The first releases should prove the governance thesis with deterministic tooling before adding broad multi-runtime orchestration.

## P0 — Architecture Contract MVP

Build first:

1. contract parser and schema validation;
2. repository/module scanner;
3. Python import/dependency graph;
4. architecture baseline snapshot;
5. deterministic rule evaluation;
6. structured PASS/FIX/BLOCK report.

Acceptance proof: run against FinTerminal, FlowTracer, and Gallop and reproduce known architecture findings/preservation rules.

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
