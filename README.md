# Möbius / 莫比乌斯

> **Operating System for AI Engineering Teams.**  
> **AI 软件工程团队操作系统。**

Möbius is a controller-first AI engineering operating system that turns persistent coding and autonomous agents into a governed software team.

It is **Codex-first, not Codex-only**: OpenAI Codex is the reference runtime, Hermes is the first planned additional runtime, and the upper engineering system remains runtime-agnostic.

Möbius 是一套以总控为核心的 AI 软件工程操作系统：把 Agent Runtime、工程治理、Git/CI、证据与长期知识统一成一个持续闭环。

> [!IMPORTANT]
> Möbius is currently **pre-alpha / architecture-first**. The target architecture is documented ahead of implementation, but engineering still advances through strict Stage Gates. The immediate goal remains proving the real Codex control loop first.

---

## Core architecture / 核心架构

```text
                         Human / Controller
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────┐
│                         MÖBIUS                           │
│                                                          │
│ Project Control   Role Registry   Task Contracts         │
│ Stage Gate        Policy          Audit                  │
│ Evidence Engine   Repository Control                     │
│ Knowledge Memory  Knowledge Projection                   │
└───────────────┬───────────────────┬──────────────────────┘
                │                   │
                │                   └──────────────→ Obsidian
                │                                  Human Knowledge
                ▼
         Agent Runtime Layer
        ┌────────┼─────────┐
        ▼        ▼         ▼
      Codex    Hermes    Future
        │        │
        └────┬───┘
             ▼
      Execution / Tools
             │
             ▼
      Git / Worktrees / CI
             │
             ▼
        PR / Merge State
             │
             └────────→ Evidence → Controller Gate
```

Short form:

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

---

## Five layers / 五大层

### 1. Agent Runtime

```text
AgentRuntime
├── CodexRuntime      # reference implementation
├── HermesRuntime     # planned second runtime
└── FutureRuntime     # explicit admission only
```

Candidate normalized interface:

```text
discover()
read_context()
attach()
dispatch()
watch()
interrupt()
collect_result()
```

Codex provides the first real product proof. Hermes extends a proven control plane rather than redefining it.

### 2. Engineering Governance

Möbius turns AI development into an explicit engineering organization:

```text
Project Control
Role Registry
Bounded Task Contracts
Stage Gate
Policy / Permission Boundaries
Controller Authority
```

Canonical stage flow:

```text
PLANNED → ADMITTED → IMPLEMENTING → SUBMITTED → REVIEWING
                                      ↑             │
                                      └── FIX ──────┤
                                                    ├── BLOCK
                                                    └── PASS
                                                         ↓
                                              MERGE_AUTHORIZED
                                                         ↓
                                                     MERGED
                                                         ↓
                                                     CLOSED
```

> **Automate evidence, not judgment.**

### 3. Evidence + Repository Control

Mechanical evidence can be collected automatically:

```text
git diff
changed files
tests / coverage
lint / type checks
build / migrations
Docker/service health
runtime errors
CI / PR state
contract deviations
```

Repository Control eventually manages:

```text
repository inspection
branch creation / reuse
worktree lifecycle
workspace-role binding
commit / push
PR creation / update
CI observation
merge authorization
merge
post-merge synchronization
```

Merge authority remains explicit. Authorization should be bound to the exact reviewed repository state, such as the PR head SHA; later code changes invalidate old approval.

### 4. Knowledge & Memory

Möbius preserves cumulative engineering memory rather than throwing away stage history:

```text
architecture decisions
stage outcomes
Controller PASS / FIX / BLOCK records
important failures and reusable fixes
runtime compatibility findings
testing/security/reliability lessons
research questions
product hypotheses
value threads
```

This structured state belongs to Möbius and remains machine-readable.

### 5. Obsidian Human Knowledge Layer

Obsidian is a **first-class human knowledge interface**, but not the runtime source of truth.

```text
Möbius structured state
        ↓
Knowledge Projection Engine
        ↓
Obsidian-compatible Markdown
        ↓
Human reading / backlinks / annotations / research
```

Default synchronization is one-way:

```text
Möbius → Obsidian
```

Planned knowledge areas include Project Memory, ADRs, Stage Records, Failures & Fixes, Engineering Knowledge, Research Threads and Value Threads.

A future bidirectional mode must have separate provenance, permission and conflict-resolution rules.

---

## Codex + Hermes

Möbius does not fuse Codex and Hermes into one giant agent. Both plug into the same governance system:

```text
                     Controller
                         │
                    Stage Gate
                         │
                  Role Resolution
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Backend Role             Research Role
        CodexRuntime            HermesRuntime
             │                       │
             └───────────┬───────────┘
                         ▼
                  Evidence Engine
                         │
                 Repository Control
                         │
                      PR / CI
                         │
                 Controller Review
                         │
                 Knowledge Projection
                         │
                      Obsidian
```

Hermes is a **planned integration**, not a currently implemented dependency. Its real integration surface must pass an explicit research/ADR gate before implementation.

---

## Bounded task contract / 有边界任务契约

Workers receive structured work packages rather than vague prompts:

```text
Project
Version / Stage
Role
Runtime
Objective
Frozen Scope
Non-goals
Allowed Files
Permission Boundary
Acceptance Criteria
Required Validation
Evidence Requirements
Failure Rules
Report Format
```

Failure classification:

```text
F1 — implementation defect      → fix current stage
F2 — runtime compatibility      → fix runtime adapter
F3 — contract defect            → Controller updates contract / ADR
F4 — architecture invalidated   → stop and explicitly redesign
```

---

## Ideal experience / 理想体验

```text
You:
Continue FlowTracer.

Möbius:
Current stage: BE-7.
Backend role resolved to CodexRuntime.
Frozen contract loaded.
Worktree prepared.
Task dispatched.
Implementation completed.
82 tests passed.
CI passed.
1 P2 issue found during independent review.
Repair task returned to Backend.
Second validation passed.
Awaiting final merge authorization.

After merge:
Stage record finalized.
Engineering knowledge extracted.
Obsidian project memory updated.
Next stage ready for admission.
```

The user thinks in **project, architecture, stage, risk and decision** — not in window switching, copy/paste, Git boilerplate or manual knowledge cleanup.

---

## Roadmap / v0.1 → v1.1

| Version | Target |
|---|---|
| **v0.1** | Codex persistent-thread discovery foundation |
| **v0.2** | structured thread/context read |
| **v0.3** | resume / persistent attachment |
| **v0.4** | bounded task dispatch |
| **v0.5** | normalized execution status |
| **v0.6** | evidence / validation manifests |
| **v0.7** | role registry + project bindings |
| **v0.8** | executable Stage Gate methodology |
| **v0.9** | minimal MCP control surface |
| **v1.0** | complete Codex-first engineering control plane |
| **v1.1** | Repository Control + workflow automation + Knowledge Projection + Hermes/multi-runtime expansion path |

The implementation remains **Codex-first**. Obsidian, Hermes and broader automation extend a proven system; they do not delay the first reliable control-loop proof.

---

## Documentation / 技术文档

- [`docs/00-PROJECT-CONTROL.md`](./docs/00-PROJECT-CONTROL.md) — governance baseline
- [`docs/02-R0-INTEGRATION-DECISION.md`](./docs/02-R0-INTEGRATION-DECISION.md) — Codex integration decision
- [`docs/10-MASTER-TECHNICAL-DESIGN.md`](./docs/10-MASTER-TECHNICAL-DESIGN.md) — master technical baseline
- [`docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md`](./docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md) — staged roadmap
- [`docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md`](./docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md) — Repository Control architecture
- [`docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md`](./docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md) — multi-runtime AI Engineering OS architecture
- [`docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md`](./docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md) — official Möbius naming + Obsidian knowledge architecture

---

## Current status / 当前状态

**Pre-alpha / architecture-first implementation.**

Current engineering priority remains:

```text
Codex v0.1
→ discover real persistent threads
→ validate on a real local Codex environment
→ Controller gate
→ read / resume / dispatch / status
```

The official product name is now **Möbius / 莫比乌斯**. `Codex Domination` remains only as the historical origin of the project.

---

## License

MIT License. See [`LICENSE`](./LICENSE).
