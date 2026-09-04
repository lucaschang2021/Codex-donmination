# Möbius Documentation Index

This index separates **canonical product/repository architecture**, **implementation guidance**, and **historical baselines**.

## Canonical architecture and governance

Read in this order:

1. [`20-MOBIUS-MASTER-ARCHITECTURE-v1.md`](20-MOBIUS-MASTER-ARCHITECTURE-v1.md) — canonical product architecture.
2. [`21-MOBIUS-ARCHITECTURE-CONTRACT.md`](21-MOBIUS-ARCHITECTURE-CONTRACT.md) — generic Architecture Contract semantics.
3. [`22-MOBIUS-CROSS-PLANE-CONTRACT.md`](22-MOBIUS-CROSS-PLANE-CONTRACT.md) — authority and data boundaries between control planes.
4. [`23-ARCHITECTURE-GATE-SPEC.md`](23-ARCHITECTURE-GATE-SPEC.md) — Architecture Gate semantics and finding model.
5. [`24-REFERENCE-PROJECT-POLICIES.md`](24-REFERENCE-PROJECT-POLICIES.md) — FinTerminal / FlowTracer / Gallop reference policy profiles.
6. [`25-MOBIUS-SYSTEM-BOUNDARIES.md`](25-MOBIUS-SYSTEM-BOUNDARIES.md) — product scope and Rasputin/project boundaries.
7. [`26-MOBIUS-GOVERNED-CHANGE-MODEL.md`](26-MOBIUS-GOVERNED-CHANGE-MODEL.md) — Change as the primary governed object.
8. [`27-IMPLEMENTATION-PRIORITIES.md`](27-IMPLEMENTATION-PRIORITIES.md) — implementation order after the architecture reset.
9. [`28-TERMINOLOGY.md`](28-TERMINOLOGY.md) — canonical terms.
10. [`29-MOBIUS-SELF-GOVERNANCE.md`](29-MOBIUS-SELF-GOVERNANCE.md) — normative engineering rules for this repository.

The machine-readable repository-level authority is [`../ARCHITECTURE.toml`](../ARCHITECTURE.toml).

## Historical implementation baselines

These documents preserve the early Codex-first exploration and remain useful implementation evidence, but they do not override the canonical architecture above:

- [`00-PROJECT-CONTROL.md`](00-PROJECT-CONTROL.md)
- [`01-ARCHITECTURE-v0.1.md`](01-ARCHITECTURE-v0.1.md)
- [`02-R0-INTEGRATION-DECISION.md`](02-R0-INTEGRATION-DECISION.md)
- [`10-MASTER-TECHNICAL-DESIGN.md`](10-MASTER-TECHNICAL-DESIGN.md)

## Current implementation truth

The current pre-alpha code baseline implements only a narrow P0 slice:

- TOML Architecture Contract loading;
- static Python AST scanning without importing target code;
- deterministic dependency / mutable-state / import-time-call / file-growth findings;
- Architecture Gate application service with injected scanner port;
- thin CLI and single composition root;
- isolated unit tests and CI self-gate.

Not yet implemented as complete product capabilities:

- baseline-vs-candidate Architecture Diff;
- Git/worktree/PR orchestration;
- exact-SHA merge authorization execution;
- Codex/Claude Code/Astra/Hermes runtime adapters;
- persistent Change/event store;
- knowledge projection;
- production security/hardening.

Documentation describing those capabilities is target architecture unless it explicitly states otherwise.
