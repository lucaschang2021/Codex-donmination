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
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ Runtime Adapter                               │
│ official openai-codex SDK / Codex App Server  │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ Persistent Codex Threads                      │
│ Backend / Frontend / Integration / Release... │
└───────────────────────────────────────────────┘
```

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

### Data flow

```text
list_threads
   ↓ select thread_id
read_thread(thread_id)
   ↓
Thread Reader
   ↓
official thread/read
   ↓
normalized events/history
```

### Core primitives

- `read_thread(thread_id, include_turns=True)`
- optional recent-event slicing
- stable event ordering

### Required design decisions

- persisted history versus live events
- truncation policy
- unknown/new upstream event handling
- sensitive payload redaction boundary

### Exit gate

Controller can discover at least two threads and inspect one selected thread's recent structured history without using the Codex UI.

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

### Invariants

- `thread/read` is not treated as a live subscription
- resume is explicit
- active/running thread semantics are surfaced rather than hidden

### Failure modes to handle

- missing rollout/history
- stale ID
- already-running thread
- runtime restart
- SDK/runtime version mismatch

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

### Dispatch contract

Every dispatch must include:

- concrete target thread ID
- task text
- caller/controller identity where available
- generated dispatch ID
- timestamp
- explicit acknowledgement/receipt

### Hard exclusions

No hidden:

- repository merge
- release action
- permission escalation
- multi-thread fanout

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

Upstream-native states may be richer, but the Controller-facing state model remains intentionally narrow.

### Exit gate

The full v0.x control loop becomes real:

```text
discover → read → resume/attach → dispatch → status → terminal result
```

No manual Codex window switching is required for this loop.

---

## v0.6 — Evidence Layer / 证据层

### Product outcome

Instead of only reporting “done”, Codex Domination collects mechanical evidence useful for Controller review.

### Architecture added

- Evidence Collector
- evidence manifest schema
- execution/result correlation
- artifact references

### Candidate evidence

- changed-file summary
- diff metadata
- test commands and outcomes
- lint/type-check outcomes
- runtime/app-server errors
- timing/duration
- task final response
- declared contract deviations

### Design rule

Evidence is automated; judgment is not.

### Exit gate

Controller receives a compact structured evidence bundle for each completed bounded task.

---

## v0.7 — Role Registry / 角色注册表

### Product outcome

Persistent threads can be mapped to stable engineering roles instead of being treated as anonymous conversations.

### Architecture added

- Role Registry
- aliases / role metadata
- explicit thread-role binding
- optional project binding

### Candidate roles

- Controller
- Backend
- Frontend
- Integration
- GitHub/Release
- Research
- Security Review

### Core primitives

- `bind_role(role, thread_id)`
- `resolve_role(role)`
- `list_roles()`

### Safety

Role aliases are convenience metadata; all control-critical operations still resolve to and display concrete thread IDs.

### Exit gate

Controller can address `Backend` or `Integration` while the system still records the exact underlying thread identity.

---

## v0.8 — Stage Gate Engine / 阶段门控引擎

### Product outcome

The user's controller-first engineering methodology becomes executable policy.

### Architecture added

- Stage Engine
- stage definitions
- entry/exit criteria
- evidence requirements
- PASS/FIX/BLOCK decisions
- immutable decision records

### Canonical workflow

```text
Controller freezes stage
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

### Important boundary

The Stage Engine tracks and enforces process state. It does not independently decide architectural quality.

### Exit gate

One real project stage can be represented end to end with explicit admission and review records.

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
Thread Registry / Reader / Dispatcher / Status / Evidence
  ↓
Official Codex Runtime Adapter
  ↓
Persistent Codex engineering roles
```

### v1.0 expected workflow

```text
1. Controller selects project/stage
2. Stage Engine confirms admission criteria
3. Role Registry resolves Backend thread
4. Controller reads recent context
5. bounded task is dispatched
6. Status Watcher tracks execution
7. Evidence Collector builds manifest
8. Controller independently reviews
9. Controller records PASS/FIX/BLOCK
10. only PASS admits next stage
```

### v1.0 Definition of Done

- persistent thread discovery
- structured history read
- safe resume
- bounded dispatch
- deterministic status
- evidence bundle
- role mapping
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

## v1.1 — Workflow Automation & Efficiency Layer / 工作流自动化与效率层

### Product outcome

After the v1.0 control plane is proven, Codex Domination begins automating the repetitive mechanics surrounding the Controller's methodology without removing Controller authority.

### Architecture added

- reusable Task Templates
- Stage Templates
- Validation Manifest generation
- context packaging
- retry/repair loop helpers
- lightweight project profiles
- cross-role handoff packets
- metrics/telemetry for workflow efficiency

### Example experience

Controller issues:

```text
Admit BE-4 for FlowTracer.
```

Codex Domination can then prepare, but not silently approve:

```text
- resolve Backend role → exact thread ID
- load frozen BE-4 task contract
- package bounded context
- dispatch implementation task
- watch execution
- collect tests/diff/evidence
- present Controller review packet
- wait for PASS/FIX/BLOCK
```

### Efficiency metrics

- manual relay steps avoided
- average Controller-to-worker round trips
- task completion latency
- repair-loop count
- evidence completeness
- failed/mis-targeted dispatch rate
- Controller context size saved

### Key methodological outcome

At v1.1, Codex Domination is no longer only a bridge. It is an executable representation of a controller-first AI software engineering methodology.

It automates the workflow around judgment while deliberately preserving the judgment itself.

---

# 5. Happy-Path Simulation / 理想顺利路径模拟

This section models the intended future system assuming each stage works as designed.

```text
Human defines product requirement
        ↓
Controller freezes architecture + stage contract
        ↓
Codex Domination resolves role/thread
        ↓
Context package generated
        ↓
Bounded task dispatched to persistent Codex worker
        ↓
Worker executes inside declared permission boundary
        ↓
Status events normalized
        ↓
Mechanical validation/evidence collected
        ↓
Controller receives review packet
        ↓
PASS ─────────────→ next stage admitted
FIX  ─────────────→ bounded repair task sent back
BLOCK─────────────→ architecture/contract decision required
```

The default failure strategy is local repair:

```text
runtime failure
  → classify
  → preserve frozen contract
  → issue bounded repair
  → rerun validation
  → Controller re-review
```

Architecture is revised only when evidence shows the frozen assumption itself is invalid.

---

# 6. Failure Taxonomy / 故障分类

Failures discovered during Codex implementation should be classified before changing design.

## F1 — Implementation defect

Examples:
- parsing bug
- invalid boundary validation
- wrong field mapping
- missing test

Action: fix in current implementation stage.

## F2 — Runtime compatibility defect

Examples:
- SDK version drift
- Windows-specific launch behavior
- App Server lifecycle issue

Action: fix Runtime Adapter or compatibility layer; preserve higher-level contracts where possible.

## F3 — Contract defect

Examples:
- ambiguous status semantics
- unsafe retry behavior
- non-deterministic target selection

Action: Controller updates the affected technical contract/ADR before implementation continues.

## F4 — Architectural invalidation

Example:
- an official supported primitive fundamentally cannot provide the required capability.

Action: stop the stage, open an ADR, revise the architecture explicitly. Never silently patch around it.

---

# 7. Codex Implementation Protocol / Codex 施工协议

Once Codex quota is available, each implementation stage should be dispatched with the same compact contract.

## Task packet

Every task contains:

- stage/version
- objective
- frozen scope
- explicit non-goals
- relevant architecture docs
- files/modules allowed to change
- acceptance criteria
- required tests
- required report format

## Developer report

Codex reports:

```text
Stage:
Status:
Changed files/modules:
Implemented contract:
Tests/validation:
Known deviations:
Risks:
Needs Controller decision:
Evidence manifest:
```

## Controller review

Controller independently checks:

- contract compliance
- hidden scope expansion
- security/permission changes
- failure semantics
- tests and evidence
- upstream compatibility assumptions

The worker never self-admits the next stage.

---

# 8. Documentation Hierarchy / 文档层级

The repository documentation should follow this authority order:

```text
00-PROJECT-CONTROL.md
        ↓
10-MASTER-TECHNICAL-DESIGN.md
        ↓
11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md
        ↓
ADR / integration decisions
        ↓
version/stage technical design
        ↓
implementation + tests
        ↓
validation / Controller admission record
```

When documents conflict, the higher-level frozen authority wins until explicitly amended.

---

# 9. Version Completion Record / 版本完成记录

Each version should eventually gain a small completion record containing:

- implementation commit/PR
- tests and CI result
- real-environment validation result
- known limitations
- Controller verdict
- exact next version admitted

This turns the repository history into an auditable record of how the architecture became real.

---

# 10. Final Direction / 最终方向

The intended evolution is:

```text
v0.1  discover
v0.2  read
v0.3  resume
v0.4  dispatch
v0.5  status
v0.6  evidence
v0.7  roles
v0.8  stage gates
v0.9  MCP
v1.0  complete controller-first control plane
v1.1  workflow automation + methodology productization
```

If every version succeeds, Codex Domination becomes the layer that manages the AI engineering organization itself:

> IDE manages code. GitHub manages versions. Codex performs work. Codex Domination manages the controlled multi-agent engineering process.
