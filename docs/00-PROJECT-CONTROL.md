# Möbius — Project Control / 项目控制基线

> Official product name: **Möbius / 莫比乌斯**  
> Historical codename: **Codex Domination**

## 1. Mission / 使命

Möbius exists to provide a controller-first operating system for AI engineering teams.

它把 Agent Runtime、工程治理、Evidence、Git/CI、长期知识与人类最终判断连接成一个结构化、可观察、可审计的开发闭环。

Möbius is not an unrestricted autonomous software factory. Its purpose is to automate execution mechanics and coordination while preserving explicit Controller authority over architecture, risk, stage admission and merge/release decisions.

Core thesis:

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

---

## 2. Architectural Identity / 架构身份

Möbius is **Codex-first, not Codex-only**.

- OpenAI Codex is the reference runtime and first implementation target.
- Hermes is the first planned additional runtime.
- Future runtimes require explicit integration research + ADR admission.
- Runtime-specific agency is separated from upper-layer governance.

Canonical target architecture:

```text
Governance Plane
Runtime Plane
Evidence Plane
Repository Plane
Knowledge Plane
```

The authoritative target-system document is:

`docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md`

---

## 3. v0.1 Frozen Objective / v0.1 冻结目标

The product identity has expanded, but **v0.1 scope remains frozen**.

Prove one reliable Codex control foundation:

```text
Controller
  → discover persistent Codex threads
  → normalize stable identities
  → validate behavior in a real local Codex environment
```

The broader read/resume/dispatch/status loop is built only through subsequent admitted stages.

v0.1 MUST NOT silently absorb:

- Hermes integration
- Obsidian synchronization
- automatic PR/merge
- broad Repository Control
- dashboard-first product work
- generic multi-runtime orchestration
- autonomous release authority

Long-range architecture is allowed to describe these capabilities; implementation gates still control when they enter the product.

---

## 4. Controller-First Governance / 总控优先治理

Canonical process:

```text
Architecture / contract frozen
        ↓
Stage admitted
        ↓
Worker role executes
        ↓
Mechanical evidence collected
        ↓
Controller independently reviews
        ↓
PASS / FIX / BLOCK
        ↓
If PASS: merge authorization may be issued
        ↓
Repository action executes
        ↓
Stage closes + knowledge is extracted
```

Rules:

1. Worker completion is not Controller approval.
2. Green tests/CI are evidence, not architectural judgment.
3. `PASS`, `MERGE_AUTHORIZED`, `MERGED`, and `CLOSED` are separate states.
4. No stage begins before the previous required gate passes.
5. New product ideas enter architecture/roadmap first, not active implementation by default.
6. Ordinary defects are repaired locally; architecture changes require explicit evidence and ADR treatment.

---

## 5. Runtime Governance / Agent Runtime 治理

The runtime abstraction exists to keep Möbius independent from any single agent provider.

```text
AgentRuntime
├── CodexRuntime
├── HermesRuntime
└── FutureRuntime
```

No runtime receives authority merely because it is capable of performing an action.

Runtime integration must define:

- identity / persistence semantics
- read/context semantics
- dispatch semantics
- status/event semantics
- interruption/recovery behavior
- permission boundary
- evidence/artifact boundary

Unsupported capabilities must fail explicitly.

---

## 6. Repository Control Governance / 仓库控制治理

Repository Control is a first-class Möbius subsystem.

Long-range automation may include:

```text
branch
worktree
commit
push
PR
CI
merge
post-merge synchronization
```

Authority rules:

1. Agent task completion never implies merge authority.
2. Merge authorization binds to a concrete PR and exact reviewed head SHA.
3. Any new commit invalidates previous authorization.
4. Dirty or unexpected workspace state blocks automation by default.
5. Destructive repository actions require higher authority than ordinary development actions.
6. Worker roles cannot self-authorize merge/release.
7. Git mechanics may be automated; Git authority remains explicit.

---

## 7. Evidence Governance / 证据治理

Mechanical evidence may include:

- git diff / changed files
- tests / coverage
- lint / type checks
- build / migrations
- Docker/service health
- runtime errors
- CI / PR state
- contract deviations

Core rule:

> **Automate evidence, not judgment.**

Evidence collection can be automatic. Controller review remains independent and risk-driven.

---

## 8. Knowledge & Obsidian Governance / 知识与 Obsidian 治理

Möbius maintains machine-readable source-of-truth knowledge.

Obsidian is a first-class **Human Knowledge Interface**, not the runtime database.

Initial direction:

```text
Möbius structured knowledge
        ↓
Knowledge Projection
        ↓
Obsidian-compatible Markdown
```

Knowledge may include:

- architecture decisions
- stage records
- Controller decisions
- failures and reusable fixes
- runtime compatibility findings
- engineering lessons
- research threads
- product hypotheses
- value threads

Bidirectional Obsidian synchronization requires a separate ADR covering provenance, conflicts and permissions.

---

## 9. Failure Taxonomy / 故障分类

```text
F1 — Implementation defect
     → repair current stage

F2 — Runtime / compatibility defect
     → repair adapter / compatibility layer

F3 — Contract defect
     → Controller updates contract / ADR

F4 — Architectural invalidation
     → stop stage, explicit redesign
```

Implementation bugs must not silently rewrite the global architecture.

---

## 10. Documentation Authority / 文档权威顺序

For target-system architecture:

```text
00-PROJECT-CONTROL.md
        ↓
20-MOBIUS-MASTER-ARCHITECTURE-v1.md
        ↓
Architecture Amendments / ADRs
        ↓
11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md
        ↓
Stage Technical Design
        ↓
Task Contract
        ↓
Implementation
```

`docs/10-MASTER-TECHNICAL-DESIGN.md` remains an important historical/implementation baseline from the Codex-first phase, but it must be interpreted through the official Möbius product identity and the newer canonical target architecture.

No implementation may silently contradict a higher-authority document.

---

## 11. Current Engineering Priority / 当前工程优先级

Despite the expanded target architecture, the immediate implementation priority remains deliberately narrow:

```text
Codex foundation
→ real persistent-thread discovery
→ real local environment validation
→ Controller gate
→ structured read
→ resume / attachment
→ bounded dispatch
→ normalized status
```

Only after these foundations are proven should later stages admit Evidence automation, Role/Project orchestration, Stage Gate execution, Repository Control, Knowledge Projection, Hermes integration and broader multi-runtime operation.

---

## 12. Definition of Long-Term Success / 长期成功定义

Möbius succeeds when a user can think primarily in:

```text
project
architecture
stage
risk
decision
```

while Möbius safely handles the repetitive mechanics of:

```text
agent routing
context transport
execution monitoring
validation evidence
Git/worktree/PR/CI
repair loops
knowledge extraction
Obsidian projection
```

without removing explicit human/Controller authority from control-critical decisions.
