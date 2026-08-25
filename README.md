# Möbius / 莫比乌斯

> **Operating System for AI Engineering Teams.**  
> **AI 软件工程团队操作系统。**

Möbius is a controller-first AI engineering operating system that turns capable agents into a governed software team.

It is **Codex-first, not Codex-only**: OpenAI Codex is the reference runtime, Hermes is the first planned additional runtime, and future runtimes can be admitted through a stable adapter boundary.

Möbius 把 Agent 执行、工程治理、Git/CI、机械证据与长期知识连接成一个持续闭环，让人类把精力放在架构、风险与决策，而不是切窗口、复制粘贴、手工 Git 和重复整理上下文。

> [!IMPORTANT]
> Möbius is currently **pre-alpha / architecture-first**. The target system is documented ahead of implementation, but implementation still advances through strict Stage Gates. The immediate engineering proof remains the real Codex control loop.

---

## The thesis / 核心命题

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

Agent runtimes provide **agency**. Möbius provides **governance**.

```text
                         Human / Controller
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────┐
│                         MÖBIUS                             │
│                                                            │
│  Governance   Runtime   Evidence   Repository   Knowledge   │
└───────────────┬──────────┬──────────┬────────────┬──────────┘
                │          │          │            │
                │          │          │            └──→ Obsidian
                │          │          │
                │          │          └──→ Git / Worktree / CI / PR
                │          │
                │          └──→ tests / diff / validation / audit
                │
                └──→ Codex / Hermes / Future Runtime
```

---

## Five planes / 五大平面

### 1. Governance Plane

Möbius turns AI work into an explicit engineering organization:

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

A worker may finish implementation. It does **not** admit the next stage.

### 2. Runtime Plane

```text
AgentRuntime
├── CodexRuntime      # reference implementation
├── HermesRuntime     # planned second runtime
└── FutureRuntime     # explicit admission only
```

Candidate normalized capabilities:

```text
discover()
read_context()
attach()
dispatch()
watch()
interrupt()
collect_result()
```

Codex remains the first product proof. Hermes extends the proven system rather than redefining it.

### 3. Evidence Plane

Möbius does not trust a worker saying “done” as sufficient proof.

Candidate evidence:

```text
git diff
changed files
tests / coverage
lint / type checks
build / migrations
Docker / service health
runtime errors
CI / PR state
contract deviations
```

> **Automate evidence, not judgment.**

Mechanical facts may be automated. Architecture, security and stage admission remain explicit Controller decisions.

### 4. Repository Plane / Git Orchestrator

Git is a first-class subsystem:

```text
repository inspection
branch creation / reuse
worktree lifecycle
role ↔ workspace binding
commit / push
PR creation / update
CI observation
merge authorization
merge
post-merge synchronization
```

Intended flow:

```text
Agent completes task
      ↓
Evidence collected
      ↓
Commit / Push / PR
      ↓
CI
      ↓
Controller review
      ↓
PASS
      ↓
MergeAuthorization bound to exact PR head SHA
      ↓
Automatic merge
      ↓
Synchronize main + worktrees
```

If reviewed code changes, old authorization becomes invalid.

> **Automate Git mechanics. Preserve Git authority.**

### 5. Knowledge Plane + Obsidian

Möbius preserves what the engineering organization learns:

```text
Architecture Decisions
Stage Records
Controller Decisions
Failures & Fixes
Runtime Compatibility Findings
Engineering Lessons
Research Threads
Product Hypotheses
Value Threads
```

Möbius keeps machine-readable source-of-truth state. Obsidian is the first-class **human knowledge interface**:

```text
Möbius structured knowledge
          ↓
Knowledge Projection Engine
          ↓
Obsidian-compatible Markdown
          ↓
Human reading / backlinks / annotation / research
```

Initial direction is one-way:

```text
Möbius → Obsidian
```

A future bidirectional mode requires separate provenance, permission and conflict-resolution rules.

---

## Codex + Hermes

Möbius does not fuse Codex and Hermes into one giant agent. They plug into the same engineering constitution.

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

Hermes is a **planned integration**, not a currently implemented dependency. Its actual integration surface must pass a dedicated research/ADR gate before implementation.

---

## Bounded engineering contracts / 有边界工程契约

Workers receive explicit task packets:

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

Ordinary bugs should not silently churn the master architecture.

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

The user thinks in **project, architecture, stage, risk and decision** — not in thread switching, copy/paste, Git boilerplate or manual knowledge cleanup.

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

The implementation remains **Codex-first**. Repository automation, Obsidian and Hermes extend a proven control plane; they do not bypass the first reliable runtime proof.

---

## Documentation / 技术文档

- [`docs/00-PROJECT-CONTROL.md`](./docs/00-PROJECT-CONTROL.md) — governance baseline
- [`docs/02-R0-INTEGRATION-DECISION.md`](./docs/02-R0-INTEGRATION-DECISION.md) — Codex integration decision
- [`docs/10-MASTER-TECHNICAL-DESIGN.md`](./docs/10-MASTER-TECHNICAL-DESIGN.md) — historical/implementation master baseline
- [`docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md`](./docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md) — staged roadmap
- [`docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md`](./docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md) — Repository Control architecture
- [`docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md`](./docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md) — multi-runtime target architecture
- [`docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md`](./docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md) — Knowledge + Obsidian architecture
- [`docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md`](./docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md) — **canonical target architecture**
- [`docs/21-MOBIUS-CROSS-PLANE-CONTRACT.md`](./docs/21-MOBIUS-CROSS-PLANE-CONTRACT.md) — cross-plane contracts and authority boundaries

Documentation authority for target-system questions should prefer `20-MOBIUS-MASTER-ARCHITECTURE-v1.md`; stage-specific implementation still remains constrained by frozen stage contracts and Controller gates.

---

## Current status / 当前状态

**Pre-alpha / architecture-first implementation.**

Immediate engineering priority:

```text
Codex foundation
→ discover real persistent threads
→ validate in a real local Codex environment
→ Controller gate
→ read / resume / dispatch / status
```

Official product name: **Möbius / 莫比乌斯**.

Historical codename: **Codex Domination**.

---

## License

MIT License. See [`LICENSE`](./LICENSE).
