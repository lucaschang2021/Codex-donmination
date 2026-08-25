# Möbius — Canonical Master Architecture / 终局总架构

> Status: **Canonical Target Architecture / 终局目标架构**
>
> Product: **Möbius / 莫比乌斯**
>
> Positioning: **Operating System for AI Engineering Teams**
>
> Historical codename: `Codex Domination`

---

## 1. Product Thesis / 产品命题

Möbius is a controller-first operating system for AI engineering teams.

It does not try to build the smartest individual coding agent. It governs multiple capable agent runtimes as one auditable engineering organization.

Möbius separates **agency** from **governance**:

- Agent runtimes provide reasoning, planning, coding, tool use and execution.
- Möbius provides project structure, role ownership, bounded contracts, evidence, repository state, stage admission, memory and final authority.

The core principle is:

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

---

## 2. The Möbius Loop / 莫比乌斯闭环

```text
Requirement / Intent
        ↓
Architecture + Contract
        ↓
Project + Stage Admission
        ↓
Role Resolution
        ↓
Agent Runtime Selection
   ┌────┼──────────┐
   ▼    ▼          ▼
 Codex Hermes    Future
   └────┼──────────┘
        ↓
Bounded Execution
        ↓
Mechanical Evidence
        ↓
Repository State / PR / CI
        ↓
Controller Review
   ┌────┼──────┐
   ▼    ▼      ▼
 PASS  FIX   BLOCK
   │    │
   │    └────────→ repair loop
   ▼
State-bound Merge Authorization
        ↓
Merge + Synchronization
        ↓
Knowledge Extraction
        ↓
Obsidian Projection
        ↓
Reusable Project Memory
        ↓
Next Requirement / Stage
        └──────────────────────────────→
```

The end of one engineering stage becomes structured context for the next. This is why the product is called **Möbius**.

---

## 3. Six System Planes / 六大系统平面

Möbius is organized into six first-class planes.

### Plane A — Agent Runtime Plane

Purpose: provide execution capability while hiding runtime-specific implementation details.

```text
AgentRuntime
├── CodexRuntime      # reference implementation
├── HermesRuntime     # planned second runtime
└── FutureRuntime     # explicit admission only
```

Normalized capabilities:

```text
discover()
read_context()
attach()
dispatch()
watch()
interrupt()
collect_result()
capabilities()
```

Codex-specific threads/turns and Hermes-specific sessions/agents remain inside adapters.

### Plane B — Orchestration Plane

Purpose: decide where work goes and package it deterministically.

```text
Project Registry
Role Registry
Runtime Routing
Context Packager
Task Contract Engine
Cross-role Handoff
Repair Loop Router
```

Every execution targets an explicit project, stage, role, runtime identity and workspace.

### Plane C — Governance Plane

Purpose: encode the engineering constitution.

```text
Stage Gate Engine
Policy Engine
Permission Boundary
Controller Authority
Decision Records
Audit Trail
```

Canonical lifecycle:

```text
PLANNED
  ↓
ADMITTED
  ↓
IMPLEMENTING
  ↓
SUBMITTED
  ↓
REVIEWING
  ├── FIX_REQUIRED → IMPLEMENTING
  ├── BLOCKED
  └── PASS
        ↓
MERGE_AUTHORIZED
        ↓
MERGED
        ↓
KNOWLEDGE_CAPTURED
        ↓
CLOSED
```

Worker completion never equals Controller approval.

### Plane D — Evidence Plane

Purpose: establish machine-verifiable facts independent of agent prose.

Candidate evidence:

```text
changed files
git diff / patch metadata
tests
coverage
lint
type checks
build
migrations
Docker/service health
runtime errors
CI checks
PR state
security scans
contract deviations
execution timing
worker result
```

Canonical artifact:

```text
ValidationManifest
```

Principle:

> **Automate evidence, not judgment.**

### Plane E — Repository Plane

Purpose: turn Git and GitHub from manual operator work into governed infrastructure.

```text
Repository Registry
Branch Manager
Worktree Manager
Workspace Guard
Commit Manager
Push Manager
PR Manager
CI Watcher
Merge Authorization Validator
Merge Executor
Post-merge Synchronizer
```

Target flow:

```text
prepare repository
→ bind worktree to role
→ execute bounded task
→ collect evidence
→ commit / push / PR
→ observe CI
→ Controller review
→ state-bound authorization
→ merge
→ synchronize main/worktrees
```

Merge authorization is bound to the exact reviewed repository state, preferably the PR head SHA. Any later mutation invalidates approval.

### Plane F — Knowledge Plane

Purpose: convert execution history into durable institutional memory.

Machine-readable knowledge remains owned by Möbius.

```text
Project Memory
Architecture Decisions
Stage Records
Failure / Fix Knowledge
Runtime Compatibility Knowledge
Engineering Patterns
Research Threads
Value Threads
```

Projection pipeline:

```text
Möbius Source of Truth
        ↓
Knowledge Extraction
        ↓
Knowledge Projection Engine
        ↓
Obsidian-compatible Markdown
        ↓
Backlinks / Maps of Content / Human Annotation
```

Obsidian is a first-class **Human Knowledge Interface**, not a runtime database.

Default synchronization:

```text
Möbius → Obsidian
```

Future bidirectional context ingestion requires provenance, conflict resolution and explicit permission design.

---

## 4. Controller / 总控

The Controller is the highest engineering authority in Möbius.

It may be implemented through ChatGPT, another approved reasoning system, a CLI/MCP client, or a future dedicated interface, but the logical authority remains stable.

Controller responsibilities:

```text
freeze architecture
admit stage
review evidence
inspect high-risk changes
record PASS / FIX / BLOCK
issue merge authorization
approve architecture changes
admit next stage
```

The Controller is intentionally not replaced by worker autonomy.

---

## 5. Role Model / 角色模型

A role is a governance identity.

Example:

```yaml
project: FlowTracer
roles:
  backend:
    runtime: codex
    agent_id: codex-thread-backend
    workspace: D:/FlowTracer-wt/backend

  frontend:
    runtime: codex
    agent_id: codex-thread-frontend
    workspace: D:/FlowTracer-wt/frontend

  research:
    runtime: hermes
    agent_id: research-01

  security_review:
    runtime: hermes
    agent_id: security-review-01

  integration:
    runtime: codex
    agent_id: codex-thread-integration
    workspace: D:/FlowTracer-wt/integration
```

Role metadata may include:

```text
runtime
agent identity
workspace/worktree
allowed paths
forbidden actions
tool profile
validation profile
evidence requirements
stage eligibility
escalation policy
```

---

## 6. Task Contract / 任务契约

Every meaningful worker execution should be bounded by a structured task packet.

```text
Project
Version
Stage
Role
Runtime
Objective
Frozen Scope
Non-goals
Allowed Files / Workspace
Permission Boundary
Acceptance Criteria
Required Validation
Evidence Requirements
Failure Rules
Report Format
```

Task Contracts are runtime-independent. Runtime adapters serialize them into the format each agent understands.

---

## 7. Codex + Hermes Strategy / Codex 与 Hermes

### Codex

Codex is the reference runtime and first product proof because the project originated from persistent multi-Codex engineering workflows.

Primary strengths inside Möbius:

```text
persistent coding contexts
repository-local implementation
bounded engineering tasks
tool execution
integration/fix loops
```

### Hermes

Hermes is the first planned additional runtime.

Primary intended roles:

```text
research
planning
cross-project analysis
security/review assistance
longer autonomous investigation
specialized recovery workflows
```

Hermes integration does not bypass the same role, task, evidence, stage and repository policies.

Before implementation, Hermes must pass an independent integration research/ADR gate.

### Future runtimes

A future runtime is admitted only when:

1. its integration surface is documented;
2. its identity/execution model can be normalized safely;
3. authority boundaries are explicit;
4. deterministic targeting is possible;
5. failure semantics are defined;
6. Controller approves the adapter contract.

---

## 8. Knowledge Architecture / 知识架构

A completed stage is not complete until valuable knowledge is preserved.

Target knowledge extraction classes:

```text
ArchitectureKnowledge
DecisionKnowledge
FailureKnowledge
FixKnowledge
RuntimeKnowledge
SecurityKnowledge
TestingKnowledge
ResearchKnowledge
ValueThreadKnowledge
```

Suggested Obsidian vault projection:

```text
Möbius Vault/
├── Projects/
├── Architecture/
├── ADR/
├── Stages/
├── Failures-and-Fixes/
├── Engineering-Knowledge/
├── Runtime-Knowledge/
├── Research/
├── Value-Threads/
├── Decisions/
└── Indexes/
```

Every generated note should carry provenance:

```yaml
managed_by: mobius
project: <project>
stage: <stage>
source_type: <source>
runtime: <runtime>
commit: <sha>
pr: <number>
created_at: <timestamp>
```

Generated content and human-authored annotations must remain distinguishable.

---

## 9. Multi-Project Operating Model / 多项目模型

One Möbius installation may manage several projects while preserving isolation.

Each project defines:

```text
repository
architecture authority
roles
runtime bindings
worktree strategy
current version/stage
task templates
validation profile
repository policy
knowledge namespace
Controller policy
```

Möbius should support a global view such as:

```text
FlowTracer        BE-7   REVIEWING
Möbius            v0.4   IMPLEMENTING
Rasputin          ARCH-2 BLOCKED
OtherProject      REL-1  CLOSED
```

---

## 10. Control Surface / 控制接口

The external control surface should stay narrow, typed and auditable.

Candidate high-level operations:

```text
project.list()
project.get_state()
role.list()
role.resolve()
runtime.list()
agent.list()
agent.read()
task.prepare()
task.dispatch()
task.status()
task.interrupt()
evidence.collect()
stage.get()
stage.review()
stage.admit()
repo.get_state()
repo.prepare_stage()
repo.open_pr()
repo.get_ci()
repo.authorize_merge()
repo.merge()
knowledge.project()
knowledge.search()
knowledge.get_context()
```

An unrestricted shell is not part of the governance surface.

---

## 11. Failure Taxonomy / 故障分类

```text
F1 Implementation Defect
   → repair inside current stage

F2 Runtime / Compatibility Defect
   → repair adapter/compatibility layer

F3 Contract Defect
   → Controller revises task/stage contract

F4 Architectural Invalidation
   → stop, issue ADR, explicitly redesign
```

Implementation failures do not silently rewrite architecture.

---

## 12. Security Invariants / 安全不变量

1. Never bypass runtime authentication, sandboxing or approval models.
2. Every execution targets an explicit runtime identity.
3. Every repository mutation targets an explicit repository state.
4. Worker completion cannot authorize merge.
5. Controller PASS is explicit and auditable.
6. Merge authorization is state-bound and invalidated by later changes.
7. Secrets are isolated by project/runtime/role boundaries.
8. Cross-role and cross-runtime handoffs are structured.
9. Destructive actions require explicit policy and audit records.
10. Obsidian never becomes an implicit authority source.
11. Human annotations cannot silently mutate machine state.
12. Architecture changes require explicit ADR/controller approval.

---

## 13. Version Strategy / 版本策略

The implementation remains deliberately staged.

```text
v0.1  Codex discovery foundation
v0.2  structured context read
v0.3  resume / attachment
v0.4  bounded dispatch
v0.5  normalized status
v0.6  evidence manifests
v0.7  roles + project binding
v0.8  Stage Gate engine
v0.9  MCP control surface
v1.0  complete Codex-first control plane
v1.1  Repository Control + workflow automation + Knowledge Projection + Hermes admission path
```

Architecture may describe the full end state, but implementation never skips stage gates to chase breadth.

---

## 14. Definition of the End State / 终局定义

Möbius succeeds when the human no longer operates individual agent windows, Git mechanics, status relays and knowledge cleanup as separate chores.

The human should operate at the level of:

```text
intent
architecture
project
stage
risk
decision
```

while Möbius governs the continuous loop beneath:

```text
Agents
→ Execution
→ Evidence
→ Repository
→ Review
→ Merge
→ Knowledge
→ Next Stage
```

That is the product boundary.

> **Möbius does not merely orchestrate agents. It turns AI-assisted development into a governed, observable, auditable and cumulative engineering system.**
