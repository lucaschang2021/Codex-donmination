# Codex Domination — Versioned Technical Roadmap v0.1 → v1.1

> Status: Architecture-first planning baseline. This document models the intended happy-path evolution before implementation is complete. Runtime failures discovered later are fixed inside the affected stage; they do not silently redefine the global architecture.

## 0. Purpose / 目的

This document converts the Codex Domination product vision into a staged technical construction plan from v0.1 through v1.1.

The core method is deliberate:

1. freeze the intended architecture first;
2. simulate the successful end-to-end workflow;
3. define narrow interfaces and acceptance gates before implementation;
4. let Codex implement one bounded stage at a time;
5. repair real-world failures in the implementation stage where they occur;
6. require Controller review before any version boundary is crossed.

The architecture is therefore the planned control system; implementation defects are local deviations to be repaired, not reasons to abandon structure by default.

---

## 1. Product Thesis / 产品命题

Codex Domination is a controller-first control plane for multiple persistent Codex agents.

It is not primarily a chatbot UI, generic agent framework, autonomous coding factory, or project-management suite.

Its responsibility is to make this loop structured, observable and auditable:

```text
Human / Controller
      ↓
Codex Domination Control Plane
      ↓
Persistent specialist Codex threads
      ↓
Execution + evidence + status
      ↓
Controller review
      ↓
PASS / FIX / BLOCK / NEXT STAGE
```

Long-term product principle:

> Automate transport, evidence, repetition and coordination. Preserve explicit judgment and authority.

---

## 2. Architectural Invariants / 不变量

These rules apply from v0.1 through v1.1 unless an explicit ADR changes them.

### 2.1 Controller remains the final authority

No stage may silently grant merge, release, destructive repository, credential, or production authority to a worker agent.

### 2.2 Thread identity is explicit

Every read, dispatch, status request and future orchestration action must target a concrete thread identity. No fuzzy hidden routing is allowed on control-critical paths.

### 2.3 Read, resume, dispatch and status are separate concerns

- discovery answers what threads exist;
- read answers what persisted history/state exists;
- resume attaches/re-attaches to a persistent thread when needed;
- dispatch starts bounded work;
- status observes execution state;
- evidence summarizes mechanical outcomes for Controller review.

### 2.4 Codex official supported surfaces are preferred

Official Codex SDK/App Server interfaces are the primary integration path. UI scraping is not a default transport.

### 2.5 Normalized internal models isolate upstream churn

Generated SDK response models must not leak throughout the application. Upstream responses are normalized at the adapter boundary.

### 2.6 Version gates are explicit

A version is not considered complete because code exists. It is complete only after:

```text
implementation
→ tests
→ real-environment validation where required
→ Controller independent review
→ documented PASS
```

---

## 3. Target System Architecture / 目标架构

```text
┌───────────────────────────────────────────────┐
│ Human / Controller                            │
│ architecture decisions + final authority      │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ Control Surface                               │
│ CLI → MCP → later optional UI/API             │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ Codex Domination Core                         │
│                                               │
│ Thread Registry                               │
│ Thread Reader                                 │
│ Task Dispatcher                               │
│ Status Watcher                                │
│ Event Normalizer                              │
│ Evidence Collector                            │
│ Stage/Policy Engine                           │
│ Audit Store                                   │
│ Repository Control Plane / Git Orchestrator   │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ Runtime + Repository Adapters                 │
│ Codex SDK/App Server + Git/GitHub/CI          │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ Persistent Codex Threads + Project Repos      │
│ Backend / Frontend / Integration / Release... │
└───────────────────────────────────────────────┘
```

Repository control is first-class in the final system. Detailed repository architecture is defined in `docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md`.

---

# 4. Version Plan / 版本计划

## v0.1 — Discovery Foundation / 发现基础

### Product outcome

Codex Domination can connect to the supported local Codex runtime and discover persistent Codex threads without mutating them.

### Architecture added

- Runtime Adapter baseline
- Thread Registry baseline
- normalized `ThreadSummary`
- read-only CLI surface

### Core capability

```text
Controller
  → Codex Domination
  → official SDK
  → thread_list
  → normalized thread list
```

### Public/internal primitives

- `list_threads(limit=None)`
- deterministic CLI rendering
- JSON output mode

### Non-goals

- thread history read
- resume
- dispatch
- status stream
- MCP
- autonomous actions

### Required evidence

- unit tests
- lint/type-quality baseline
- CI
- real local Codex installation successfully returns thread data or a valid empty list

### Exit gate

Controller can discover persistent threads reliably and inspect stable normalized IDs.

---

## v0.2 — Thread Read Bridge / 对话读取桥

### Product outcome

Controller can select one discovered thread and read its persisted history/state without manual copy-paste.

### Architecture added

- Thread Reader
- normalized `ThreadDetail`
- normalized `ThreadEvent`
- pagination/history handling
- deterministic missing-thread errors

### Core primitives

- `read_thread(thread_id, include_turns=True)`
- optional recent-event slicing
- stable event ordering

### Exit gate

Controller can inspect one selected persistent thread's recent structured history without using the Codex UI.

---

## v0.3 — Resume & Attachment / 恢复与重新接入

### Product outcome

Codex Domination can re-attach to an existing persistent thread safely when live interaction is required.

### Architecture added

- Thread Attachment Manager
- resume lifecycle state
- thread availability classification

### Core primitives

- `resume_thread(thread_id)`
- `get_attachment_state(thread_id)`

### Exit gate

A persisted thread can be rejoined deterministically and its attachment state is observable.

---

## v0.4 — Bounded Task Dispatch / 有边界任务派发

### Product outcome

Controller can send one explicit bounded task to one specific persistent Codex thread.

### Architecture added

- Task Dispatcher
- `DispatchRequest`
- `DispatchReceipt`
- idempotency/retry policy
- task metadata

### Core primitive

- `send_task(thread_id, prompt, metadata=None)`

### Hard exclusions

No hidden repository merge, release action, permission escalation, or multi-thread fanout.

### Exit gate

Controller can target one known thread, submit one bounded task, and receive a deterministic receipt.

---

## v0.5 — Execution Status / 执行状态观测

### Product outcome

Controller can observe whether a dispatched task is queued/running/completed/failed/interrupted/timed-out.

### Architecture added

- Status Watcher
- Event Normalizer expansion
- normalized `ExecutionStatus`
- terminal-state semantics
- timeout semantics

### Canonical state model

```text
UNKNOWN
  ↓
ACCEPTED
  ↓
RUNNING
  ├── COMPLETED
  ├── FAILED
  ├── INTERRUPTED
  └── TIMED_OUT
```

### Exit gate

The full v0.x control loop becomes real:

```text
discover → read → resume/attach → dispatch → status → terminal result
```

---

## v0.6 — Evidence Layer / 证据层

### Product outcome

Instead of only reporting “done”, Codex Domination collects mechanical evidence useful for Controller review.

### Architecture added

- Evidence Collector
- evidence manifest schema
- execution/result correlation
- artifact references
- **read-only repository evidence** via Git Orchestrator G0

### Candidate evidence

- `git status` summary
- changed-file summary
- diff metadata
- base/head SHAs
- test commands and outcomes
- lint/type-check outcomes
- runtime/app-server errors
- timing/duration
- task final response
- declared contract deviations

### Design rule

Evidence is automated; judgment is not.

### Exit gate

Controller receives a compact structured evidence bundle for each completed bounded task, including repository state.

---

## v0.7 — Role Registry / 角色注册表

### Product outcome

Persistent threads can be mapped to stable engineering roles instead of being treated as anonymous conversations.

### Architecture added

- Role Registry
- aliases / role metadata
- explicit thread-role binding
- project binding
- **repository / branch / worktree binding**

### Candidate roles

- Controller
- Backend
- Frontend
- Integration
- GitHub/Release
- Research
- Security Review

### Safety

Role aliases are convenience metadata; all control-critical operations still resolve to concrete thread IDs and concrete repository/worktree bindings.

### Exit gate

Controller can address `Backend` or `Integration` while the system records the exact underlying thread, branch and worktree identity.

---

## v0.8 — Stage Gate Engine / 阶段门控引擎

### Product outcome

The controller-first engineering methodology becomes executable policy.

### Architecture added

- Stage Engine
- stage definitions
- entry/exit criteria
- evidence requirements
- PASS/FIX/BLOCK decisions
- immutable decision records
- **stage-specific repository policy and workspace admission**

### Canonical workflow

```text
Controller freezes stage
      ↓
Repository workspace validated
      ↓
Role admitted
      ↓
Task dispatched
      ↓
Execution
      ↓
Evidence collected
      ↓
Controller review
      ↓
PASS / FIX / BLOCK
      ↓
Next stage admitted or returned for repair
```

### Exit gate

One real project stage can be represented end to end with explicit admission, repository state and review records.

---

## v0.9 — Minimal MCP Control Surface / MCP 最小控制面

### Product outcome

An external Controller such as ChatGPT can operate Codex Domination through a narrow structured tool interface.

### Architecture added

- MCP Server
- typed tool schemas
- permission boundary
- tool-to-core adapter

### Minimum tool set

- `list_threads`
- `read_thread`
- `resume_thread`
- `send_task`
- `get_status`
- `get_evidence`
- `list_roles`
- `get_stage`
- narrow repository/status primitives where needed

### Non-goals

- generic unrestricted shell
- arbitrary repository mutation
- automatic merge/release
- broad file-management API

### Exit gate

A Controller can execute the basic workflow entirely through the structured external control surface.

---

## v1.0 — Controller-First Multi-Codex Workflow / 正式控制闭环

### Product outcome

Codex Domination becomes a usable pre-production control plane for the multi-Codex engineering workflow.

### Integrated architecture

```text
Controller
  ↓
MCP Control Surface
  ↓
Stage Gate Engine
  ↓
Role Registry
  ↓
Thread + Task + Status + Evidence Core
  ↓
Repository Control Plane / Git Orchestrator
  ↓
Official Codex Runtime + Git/GitHub/CI
  ↓
Persistent Codex engineering roles + project worktrees
```

### v1.0 expected workflow

```text
1. Controller selects project/stage
2. Stage Engine confirms admission criteria
3. Git Orchestrator validates repository/worktree state
4. Role Registry resolves Backend thread + workspace
5. Controller reads recent context
6. bounded task is dispatched
7. Status Watcher tracks execution
8. Evidence Collector builds manifest including Git state
9. Controller independently reviews
10. Controller records PASS/FIX/BLOCK
11. only PASS admits next stage
```

### v1.0 Definition of Done

- persistent thread discovery
- structured history read
- safe resume
- bounded dispatch
- deterministic status
- evidence bundle
- role mapping
- branch/worktree-aware workspace validation
- stage gates
- MCP interface
- audit records
- reproducible end-to-end demo
- documented permission/threat boundaries
- no known P1 issue

### Explicitly still excluded

- autonomous merge/release authority
- fully autonomous product management
- general multi-model agent platform
- large dashboard as a core dependency

---

## v1.1 — Workflow + Git Automation / 工作流与 Git 自动化层

### Product outcome

After the v1.0 control plane is proven, Codex Domination automates the repetitive mechanics surrounding the Controller's methodology — including ordinary Git/GitHub operations — without removing Controller authority.

### Architecture added

- reusable Task Templates
- Stage Templates
- Validation Manifest generation
- context packaging
- retry/repair loop helpers
- lightweight project profiles
- cross-role handoff packets
- metrics/telemetry for workflow efficiency
- **Git Orchestrator G1–G4 automation**

### Git automation scope

Codex Domination may automatically:

- create/reuse stage branches
- create/reuse role worktrees
- verify correct workspace before dispatch
- inspect changes
- prepare validated commits
- push feature branches
- create/update PRs
- watch CI
- collect review/CI evidence
- execute a merge **only after explicit Controller authorization bound to the exact current head SHA**
- synchronize main/worktrees after merge

### Critical invariant

```text
Tests PASS ≠ Merge Authorization
CI PASS ≠ Merge Authorization
Worker says DONE ≠ Merge Authorization
PR mergeable ≠ Merge Authorization

Only:
Controller PASS
+ explicit MergeAuthorization
+ matching authorized head SHA
→ Git Orchestrator may execute merge
```

### Example experience

Controller issues:

```text
Admit BE-4 for FlowTracer.
```

Codex Domination can then:

```text
- resolve Backend role → exact thread ID
- validate/create Backend branch + worktree
- load frozen BE-4 task contract
- package bounded context
- dispatch implementation task
- watch execution
- collect tests/diff/repository evidence
- prepare commit + push branch
- open/update PR
- watch CI
- present Controller review packet
- wait for PASS/FIX/BLOCK
```

If FIX:

```text
- create bounded repair packet
- return it to the same worker
- collect new evidence
- update commit/PR/CI state
- present Controller re-review packet
```

If PASS:

```text
- Controller issues merge authorization
- authorization is bound to exact PR head SHA
- Git Orchestrator executes authorized merge
- syncs repository/worktrees
- archives stage evidence
- Stage Engine admits next stage
```

### Key methodological outcome

At v1.1, Codex Domination is no longer merely a bridge. It is an executable representation of a controller-first AI software engineering methodology in which both Codex coordination and repository choreography are automated.

The human thinks in **project → stage → role → evidence → decision** rather than thread windows, branch commands, worktree commands and PR mechanics.

---

# 5. Happy-Path Simulation / 理想顺利路径模拟

```text
Human defines product requirement
        ↓
Controller freezes architecture + stage contract
        ↓
Git Orchestrator prepares/validates workspace
        ↓
Codex Domination resolves role/thread
        ↓
Context package generated
        ↓
Bounded task dispatched to persistent Codex worker
        ↓
Worker executes inside declared permission + worktree boundary
        ↓
Status events normalized
        ↓
Mechanical validation + Git evidence collected
        ↓
Commit / push / PR / CI mechanics automated by policy
        ↓
Controller receives review packet
        ↓
PASS ─────────────→ explicit merge authorization → Git Orchestrator merge → next stage
FIX  ─────────────→ bounded repair task → new evidence → re-review
BLOCK─────────────→ architecture/contract decision required
```

The default failure strategy remains local repair. Architecture is revised only when evidence shows the frozen assumption itself is invalid.

---

# 6. Failure Taxonomy / 故障分类

## F1 — Implementation defect

Parsing bugs, validation mistakes, wrong field mappings, missing tests. Fix in current implementation stage.

## F2 — Runtime/repository compatibility defect

SDK drift, Windows launch behavior, Git/worktree/provider differences. Fix adapter/compatibility layer while preserving higher-level contracts where possible.

## F3 — Contract defect

Ambiguous status semantics, unsafe retry behavior, non-deterministic routing, unsafe merge semantics. Controller updates the affected technical contract/ADR before implementation continues.

## F4 — Architectural invalidation

A supported primitive fundamentally cannot provide the required capability. Stop the stage, open an ADR, revise architecture explicitly.

---

# 7. Documentation Authority / 文档权威层级

When implementation begins, Codex should resolve conflicts in this order:

```text
1. docs/00-PROJECT-CONTROL.md
2. docs/10-MASTER-TECHNICAL-DESIGN.md
3. docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md
4. docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md
5. accepted ADR / integration decision
6. stage-specific technical design
7. task packet
8. implementation comments
```

Architecture changes move upward through explicit review rather than being silently introduced in code.

---

# 8. Codex Task Packet Contract / Codex 施工任务包

Every future implementation task should contain:

```text
Version / Stage
Objective
Frozen Scope
Non-goals
Allowed Modules / Files
Repository / Branch / Worktree Binding
Required Interfaces
Acceptance Criteria
Required Tests
Evidence Required
Forbidden Actions
Developer Report Format
```

Developer reports completion; Controller decides admission.

---

# 9. Final v1.1 Product Shape / 最终形态

```text
User / Controller
      │
      │ "Continue FlowTracer"
      ▼
Codex Domination
      │
      ├─ knows project
      ├─ knows current stage
      ├─ knows role/thread
      ├─ knows repo/branch/worktree
      ├─ prepares task
      ├─ dispatches Codex
      ├─ observes status
      ├─ gathers tests + Git evidence
      ├─ commits/pushes/opens PR by policy
      ├─ watches CI
      ├─ routes FIX loops
      └─ waits for Controller merge authorization
              │
              ▼
        authorized merge
              │
              ▼
          next stage
```

The user should no longer manually manage Codex windows **or routine Git choreography**.

The final product thesis becomes:

> Codex Domination is the control plane for an AI software engineering organization: it coordinates persistent Codex workers, enforces the engineering method, manages repository mechanics, collects evidence, and preserves explicit human/Controller authority at the decisions that matter.
