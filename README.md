# Möbius

**Controller-first operating system for AI engineering teams, built around persistent agent runtimes, stage-gated governance, verifiable evidence, repository automation, checkpointed recovery, and long-term knowledge memory.**

[简体中文](README.zh-CN.md) · [Master Architecture](docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md) · [Roadmap](docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md) · [Checkpoint / Recovery](docs/22-CHECKPOINT-RECOVERY-ARCHITECTURE.md) · [Knowledge / Obsidian](docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md) · [Git Orchestrator](docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md) · [MIT](LICENSE)

> **Status:** Möbius is a pre-alpha, architecture-first open-source project. The target architecture is intentionally documented ahead of implementation. The immediate engineering objective is to prove a reliable Codex control loop before expanding into the full operating system.

## Why Möbius?

AI coding agents can already write, test, inspect, and modify software. The harder problem is coordinating several persistent agents as a disciplined engineering organization: deciding who may do what, preserving project context, collecting evidence, controlling Git state, surviving interrupted execution, reviewing risk, admitting stages, and retaining what the team learns.

Möbius turns that coordination layer into infrastructure.

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

Möbius is **Codex-first, not Codex-only**. OpenAI Codex is the reference runtime. Hermes is the first planned additional runtime. Future runtimes can be admitted through a stable adapter boundary without redefining the governance model.

## Core architecture

Möbius is organized around five explicit planes:

| Plane | Responsibility |
|---|---|
| Governance | Project control, role registry, bounded task contracts, Stage Gates, policy, Controller authority |
| Runtime | CodexRuntime first; HermesRuntime planned; future agent runtimes behind a normalized adapter |
| Evidence | Execution state, diffs, tests, validation manifests, CI facts, audit evidence |
| Repository | Git/worktree lifecycle, commit, push, PR, CI observation, exact-state merge authorization, synchronization |
| Knowledge | Structured engineering memory and Obsidian-compatible human knowledge projection |

Checkpoint & Recovery is a cross-cutting reliability subsystem spanning all five planes.

```text
                         Human / Controller
                                  |
                                  v
+------------------------------------------------------------+
|                           MOBIUS                           |
|                                                            |
|  Governance   Runtime   Evidence   Repository   Knowledge   |
+---------------+----------+----------+------------+----------+
                |          |          |            |
                |          |          |            +--> Obsidian
                |          |          +--> Git / Worktree / CI / PR
                |          +--> tests / diff / validation / audit
                +--> Codex / Hermes / future runtimes
```

## Controller-first governance

A worker finishing code does not mean a stage is complete. Möbius separates execution from authority.

```text
PLANNED -> ADMITTED -> IMPLEMENTING -> SUBMITTED -> REVIEWING
                                      ^              |
                                      +---- FIX -----+
                                                     +--> BLOCK
                                                     +--> PASS
                                                           |
                                                           v
                                                  MERGE_AUTHORIZED
                                                           |
                                                           v
                                                        MERGED
                                                           |
                                                           v
                                                        CLOSED
```

Mechanical work can be automated aggressively. Architecture, risk acceptance, security-sensitive decisions, stage admission, and merge authority remain explicit governance decisions.

## Agent runtimes

```text
AgentRuntime
├── CodexRuntime      # reference implementation
├── HermesRuntime     # planned second runtime
└── FutureRuntime     # explicit admission only
```

The normalized runtime boundary is expected to cover capabilities such as discovery, context reading, persistent attachment, bounded task dispatch, status observation, interruption, and result collection.

Codex is the first implementation proof. Hermes extends the proven control plane rather than replacing it.

## Evidence-first engineering

Möbius does not treat an agent saying `done` as sufficient proof. The Evidence Plane can collect machine-verifiable facts such as changed files, Git diffs, tests, coverage, lint/type checks, builds, migrations, Docker/service health, runtime errors, CI state, PR state, and contract deviations.

> **Automate evidence, not judgment.**

Evidence reduces repeated context and manual reporting while preserving independent Controller review.

## Checkpoint & Recovery

Long-running agent work must survive quota exhaustion, runtime disconnects, crashes, host restarts, and transport loss.

Möbius protects **engineering state, not model memory**. A durable checkpoint can bind the frozen task contract to the exact project, role, runtime identity, branch/worktree, last-good commit, dirty-diff identity, completed/current/remaining work, validation results, and known risks.

A recovered task follows an explicit lifecycle:

```text
RUNNING
  -> CHECKPOINTED
  -> INTERRUPTED_QUOTA / INTERRUPTED_RUNTIME / INTERRUPTED_HOST
  -> RECOVERY_PENDING
  -> RECOVERING
  -> RECOVERY_VERIFIED
  -> RUNNING
```

Recovery verifies the contract, Git/worktree state, diff, and targeted tests before execution resumes. A plain `continue` instruction is not considered safe recovery.

Where runtime quota is observable, Möbius may shrink task packets and increase checkpoint frequency as quota falls. If quota cannot be observed reliably, the system must not invent it.

## Repository Control / Git Orchestrator

Git is a first-class subsystem rather than a collection of shell commands delegated to agents.

The target Repository Plane covers repository inspection, branch creation/reuse, worktree lifecycle, role-to-workspace binding, commit/push, PR creation/update, CI observation, merge authorization, merge execution, and post-merge synchronization.

A merge authorization is bound to the exact reviewed PR head SHA. If the reviewed code changes, the previous authorization becomes invalid.

> **Automate Git mechanics. Preserve Git authority.**

## Knowledge memory and Obsidian

Möbius preserves what an AI engineering organization learns: architecture decisions, stage records, Controller decisions, failures and fixes, runtime compatibility findings, engineering lessons, research threads, product hypotheses, and value threads.

Machine-readable Möbius state remains the engineering source of truth. Obsidian is the first-class human knowledge interface:

```text
Möbius structured knowledge
          |
          v
Knowledge Projection Engine
          |
          v
Obsidian-compatible Markdown
          |
          v
Human reading / backlinks / annotation / research
```

The initial direction is one-way (`Möbius -> Obsidian`). Any future bidirectional mode requires explicit provenance, permissions, and conflict-resolution rules.

## Bounded engineering contracts

Workers receive explicit task packets rather than unconstrained goals. A contract can define project, version/stage, role, runtime, objective, frozen scope, non-goals, allowed files, permission boundaries, acceptance criteria, validation, evidence requirements, failure rules, report format, checkpoint policy, and recovery validation.

Möbius classifies failures so ordinary implementation defects do not silently rewrite the architecture:

| Class | Meaning | Default response |
|---|---|---|
| F1 | Implementation defect | Fix within the current stage |
| F2 | Runtime compatibility issue | Fix the runtime adapter |
| F3 | Contract defect | Controller updates the contract / ADR |
| F4 | Architecture invalidated | Stop and explicitly redesign |

## Ideal experience

```text
You:
Continue FlowTracer.

Möbius:
Current stage: BE-7.
Backend role resolved to CodexRuntime.
Frozen contract loaded.
Worktree prepared.
Task dispatched.
Checkpoint cp_BE-7_003 verified.
Runtime quota exhausted; task safely suspended.
Quota restored.
Repository and targeted tests revalidated.
Task resumed from checkpoint.
Implementation completed.
82 tests passed.
CI passed.
Awaiting final merge authorization.

After merge:
Stage record finalized.
Engineering knowledge extracted.
Obsidian project memory updated.
Next stage ready for admission.
```

The goal is for the human to think in project, architecture, stage, risk, and decision — not thread switching, copy/paste, Git boilerplate, interrupted-task reconstruction, or manual knowledge cleanup.

## Roadmap

| Version | Target |
|---|---|
| **v0.1** | Codex persistent-thread discovery foundation |
| **v0.2** | Structured thread/context read |
| **v0.3** | Resume / persistent attachment |
| **v0.4** | Bounded task dispatch + task identity |
| **v0.5** | Normalized execution + interruption states |
| **v0.6** | Evidence manifests + durable checkpoint/recovery prototype |
| **v0.7** | Role/project/worktree-aware checkpoint binding |
| **v0.8** | Executable Stage Gate + recovery policy |
| **v0.9** | Minimal MCP control + recovery surface |
| **v1.0** | Complete Codex-first engineering control plane with reliable interrupted-task recovery |
| **v1.1** | Repository automation + quota-aware checkpointing + Knowledge Projection + Hermes/multi-runtime expansion |

Repository automation, Obsidian, checkpoint automation, and Hermes extend a proven control plane; they do not bypass the first reliable runtime proof.

## Documentation

- [`docs/00-PROJECT-CONTROL.md`](docs/00-PROJECT-CONTROL.md) — governance baseline
- [`docs/02-R0-INTEGRATION-DECISION.md`](docs/02-R0-INTEGRATION-DECISION.md) — Codex integration decision
- [`docs/10-MASTER-TECHNICAL-DESIGN.md`](docs/10-MASTER-TECHNICAL-DESIGN.md) — CodexRuntime implementation baseline
- [`docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md`](docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md) — staged roadmap
- [`docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md`](docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md) — Repository Control architecture
- [`docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md`](docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md) — multi-runtime architecture
- [`docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md`](docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md) — Knowledge + Obsidian architecture
- [`docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md`](docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md) — canonical whole-product target architecture
- [`docs/21-MOBIUS-CROSS-PLANE-CONTRACT.md`](docs/21-MOBIUS-CROSS-PLANE-CONTRACT.md) — cross-plane contracts and authority boundaries
- [`docs/22-CHECKPOINT-RECOVERY-ARCHITECTURE.md`](docs/22-CHECKPOINT-RECOVERY-ARCHITECTURE.md) — interrupted-task durability and verified recovery

## Current status

**Pre-alpha / architecture-first implementation.**

The immediate engineering sequence is deliberately narrow:

```text
Codex foundation
-> discover real persistent threads
-> validate in a real local Codex environment
-> Controller gate
-> read / resume / dispatch / status
```

The full architecture is documented now so later implementation can fill a stable target rather than redesigning the product at every stage.

## License

Möbius is licensed under the [MIT License](LICENSE).

---

If Möbius matches how you want AI engineering teams to work, testing the early runtime loop, opening an issue, contributing an adapter, or starring the repository all help the project mature.
