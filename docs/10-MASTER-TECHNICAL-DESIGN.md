# Codex Domination — Master Technical Design / 总技术设计

> Status: **Architecture Baseline / 架构基线**
>
> This document defines the intended system architecture, module boundaries, control model, delivery sequence, security model, and acceptance gates for Codex Domination. Stage-specific documents may refine implementation details, but they must not silently contradict this baseline.
>
> 本文档定义 Codex Domination 的总体系统架构、模块边界、控制模型、交付顺序、安全边界与阶段验收门。后续阶段文档可以细化实现，但不得静默违反本基线。

---

## 1. Product Thesis / 产品命题

Codex Domination is a **controller-first orchestration layer for persistent Codex agents**.

Codex Domination 是一个**以总控为核心、面向持久化 Codex Agent 的编排控制层**。

The product is designed for software workflows where multiple persistent Codex threads act as specialized engineering roles — for example backend, frontend, integration, review, and release — while one controller maintains global context, stage admission, review authority, and task routing.

项目面向这样的软件工程工作流：多个长期存在的 Codex thread 分别承担后端、前端、集成、审查、发布等专业角色，而一个总控统一掌握全局上下文、阶段准入、复核权和任务路由。

The project does **not** attempt to replace Codex, bypass its sandbox/approval model, or build a generic autonomous agent swarm.

本项目**不**替代 Codex、不绕过 Codex 的沙箱/审批机制，也不以构建通用自主 Agent 群为目标。

---

## 2. Core Problem / 核心问题

Persistent multi-Codex workflows currently suffer from a missing control plane:

- humans manually switch between conversations;
- instructions are repeatedly copied and reformatted;
- execution state is fragmented;
- stage handoff evidence is reconstructed manually;
- controller context is wasted on mechanical relay;
- review and release boundaries are easy to blur.

当前多 Codex 持久化工作流缺少一个真正的控制平面：

- 人工切换多个会话；
- 任务指令反复复制和重写；
- 执行状态分散；
- 阶段交接证据依赖人工重建；
- 总控上下文浪费在机械中转；
- 审查、合并、发布边界容易模糊。

Codex Domination turns this relay layer into a structured, observable, permission-aware bridge.

---

## 3. Architectural Principles / 架构原则

1. **Controller first** — developer agents execute; the controller admits stages and makes final decisions.
2. **Persistent roles** — long-lived threads are preferred over disposable prompts.
3. **Official interfaces first** — use supported Codex SDK/App Server surfaces before private transport or UI automation.
4. **Structured state** — thread, turn, task and evidence data should be machine-readable.
5. **Automate evidence, not judgment** — validation collection may be automated; architectural/security review remains explicit.
6. **Least authority** — each stage exposes only the capabilities it needs.
7. **Deterministic targeting** — commands must identify an exact thread/role; no ambiguous dispatch.
8. **Observable execution** — task lifecycle must expose clear submitted/running/completed/failed/timeout states.
9. **Stage-gated delivery** — no stage begins before the previous stage exits its acceptance gate.
10. **Small control surface** — v0.1 proves the control loop before adding dashboards, GitHub automation, or broad integrations.

---

## 4. System Context / 系统上下文

```text
                         Human / Product Owner
                                  │
                                  ▼
                         Controller / 总控
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │    Codex Domination    │
                     │      Control Plane     │
                     └───────────┬────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               ▼                 ▼                 ▼
        Thread Registry       Dispatcher       Status/Event Layer
               │                 │                 │
               └─────────────────┼─────────────────┘
                                 ▼
                   Official Codex SDK / App Server
                                 │
          ┌──────────────┬───────┼────────┬──────────────┐
          ▼              ▼       ▼        ▼              ▼
       Backend        Frontend  Integration  Review     Release
        Codex           Codex      Codex      Codex       Codex
```

The Controller is a logical role, not necessarily a single UI. In v0.1 it may be a CLI/MCP client; later it may be ChatGPT, another orchestration service, or a purpose-built UI.

总控是逻辑角色，不绑定具体 UI。v0.1 中可以是 CLI/MCP 客户端；未来可以是 ChatGPT、其他编排服务或专用控制台。

---

## 5. Upstream Integration Baseline / 上游集成基线

The preferred integration path is the official OpenAI Codex Python SDK backed by the local Codex App Server.

首选集成路径：**OpenAI 官方 Codex Python SDK + 本地 Codex App Server**。

Confirmed upstream primitives include:

- `thread_list(...)`
- `thread.read(...)` / `thread_read(...)`
- `thread_resume(thread_id, ...)`
- turn execution through `thread.run(...)` / `thread.turn(...)`
- turn-scoped event streaming and terminal status

Key architectural distinction:

- **read** is snapshot/history access;
- **resume** reattaches to a persistent thread;
- **turn/run** performs new work;
- **stream/status** observes active work.

The bridge must preserve those distinctions rather than collapsing them into one generic "thread" operation.

---

## 6. Logical Modules / 逻辑模块

### 6.1 Runtime Adapter

Responsibilities:

- initialize and close the official Codex runtime;
- expose a narrow internal adapter instead of leaking SDK details everywhere;
- normalize upstream exceptions;
- own compatibility checks against SDK/runtime versions.

Candidate module:

```text
runtime.py
CodexRuntime
```

### 6.2 Thread Registry

Responsibilities:

- discover persistent threads;
- normalize thread metadata;
- maintain deterministic identifiers;
- optionally map human roles (`backend`, `frontend`, etc.) to thread IDs later.

Core internal model:

```text
ThreadSummary
- thread_id
- name
- cwd
- preview
- updated_at
- status?        # only when upstream semantics are reliable
- role?          # later controller metadata, not upstream truth
```

### 6.3 Thread Reader

Responsibilities:

- read one selected thread;
- optionally include turns/history;
- normalize messages/items/events into controller-readable structures;
- never mutate the thread.

### 6.4 Dispatcher

Responsibilities:

- explicitly target one known thread;
- resume/attach when required;
- submit one bounded task/turn;
- return a task/turn identifier;
- never infer merge/release authority from task text.

### 6.5 Status & Event Watcher

Responsibilities:

- observe one active task/turn;
- map upstream events to stable internal lifecycle states;
- detect completion/failure/interruption/timeout;
- avoid treating stale snapshots as live status.

Proposed internal lifecycle:

```text
SUBMITTED
RUNNING
WAITING_APPROVAL
COMPLETED
FAILED
INTERRUPTED
TIMED_OUT
UNKNOWN
```

### 6.6 Evidence Collector

Targeted for v0.2, not v0.1.

Responsibilities:

- changed files / diff metadata;
- test/lint/type-check evidence;
- task completion manifest;
- structured handoff to Controller.

Example:

```yaml
stage: BE-3
thread_id: ...
status: completed
changed_files: 7
validation:
  pytest: pass
  ruff: pass
controller_review_required: true
```

### 6.7 MCP Control Surface

The external control API must remain narrow.

Candidate v0.1 surface:

```text
codex.list_threads()
codex.read_thread(thread_id)
codex.send_task(thread_id, prompt)
codex.get_status(task_or_turn_id)
```

Exact names and schemas are frozen only after implementation evidence exists.

### 6.8 Controller Policy Layer

Targeted after the v0.1 control loop is stable.

Responsibilities:

- role mapping;
- stage admission;
- required evidence rules;
- PASS / FIX / BLOCK decisions;
- next-stage routing.

This layer **must not** silently auto-merge or auto-release in v0.x.

---

## 7. Data Model / 数据模型

The bridge should distinguish upstream identities from local orchestration identities.

```text
Thread
  thread_id              # Codex upstream identity
  name
  cwd
  preview
  updated_at

Task
  task_id                 # Codex Domination identity
  thread_id
  stage_id
  prompt_hash
  created_at
  state

TurnBinding
  task_id
  upstream_turn_id

Event
  task_id
  upstream_type
  normalized_type
  timestamp
  payload

Stage
  stage_id
  status
  admitted_at
  completed_at
  controller_decision
```

v0.1 may keep most structures in memory. Persistent storage is not mandatory until the control loop proves useful.

---

## 8. Control Flow / 控制流程

### 8.1 Discovery

```text
Controller
   → list_threads
   → Runtime Adapter
   → Codex SDK thread_list
   → normalize
   → ThreadSummary[]
```

### 8.2 Read

```text
Controller
   → read_thread(thread_id)
   → validate target
   → Codex SDK read
   → normalize history
   → snapshot
```

### 8.3 Dispatch

```text
Controller
   → send_task(thread_id, prompt)
   → validate target
   → resume/attach thread
   → start turn
   → bind local task_id ↔ upstream turn_id
   → return accepted task
```

### 8.4 Observe

```text
Controller
   → get/watch status(task_id)
   → event watcher
   → upstream turn stream
   → normalize state
   → terminal result / pending approval / failure
```

### 8.5 Stage Gate

```text
Controller admits stage
        ↓
Role thread receives bounded task
        ↓
Codex executes
        ↓
Bridge collects state/evidence
        ↓
Controller independently reviews
        ↓
PASS ─────→ merge/next stage
FIX  ─────→ same role receives correction task
BLOCK─────→ stop and escalate
```

---

## 9. Error Model / 错误模型

Errors must be explicit and machine-readable.

Proposed categories:

```text
RUNTIME_UNAVAILABLE
SDK_INCOMPATIBLE
AUTH_REQUIRED
THREAD_NOT_FOUND
THREAD_AMBIGUOUS
THREAD_UNAVAILABLE
INVALID_ARGUMENT
DISPATCH_REJECTED
APPROVAL_REQUIRED
TURN_FAILED
TURN_INTERRUPTED
TURN_TIMEOUT
TRANSPORT_CLOSED
UPSTREAM_PROTOCOL_ERROR
INTERNAL_ERROR
```

CLI and MCP layers should expose concise messages while preserving a structured code.

No blanket retry for non-idempotent dispatch operations.

---

## 10. Security & Permission Model / 安全与权限模型

Codex Domination is a control plane, so incorrect authority amplification is a primary risk.

Rules:

1. Never bypass Codex authentication, sandboxing, approval policy, or tool permission boundaries.
2. Thread discovery/read are lower authority than dispatch and must remain separable.
3. Dispatch requires an explicit target thread.
4. Any approval requested by Codex remains visible and explicit.
5. The bridge does not convert task completion into merge/release authorization.
6. GitHub write actions are outside v0.1.
7. Secrets must not be logged in normalized events or handoff manifests.
8. Future remote access must authenticate both controller and host.
9. Dangerous unattended actions are out of scope for early releases.

Threats to review explicitly:

- wrong-thread task delivery;
- prompt/content injection across role boundaries;
- permission escalation via delegated tool use;
- stale completion state;
- replay/duplicate dispatch;
- runtime version drift;
- event loss/reordering;
- controller spoofing in future remote mode.

---

## 11. Compatibility Strategy / 兼容策略

The official SDK/App Server may evolve quickly.

Therefore:

- all upstream interaction goes through Runtime Adapter;
- internal models remain deliberately smaller than SDK models;
- generated SDK model classes are not used as the project's public API;
- integration tests must exercise the real installed runtime where possible;
- supported SDK/runtime versions should be recorded per release;
- unknown upstream fields are ignored unless needed;
- missing required fields fail deterministically.

---

## 12. Testing Strategy / 测试策略

### Unit tests

- normalization;
- input validation;
- lifecycle mapping;
- error mapping;
- deterministic rendering.

### Contract tests

- adapter calls expected official SDK methods;
- no private JSON-RPC dependency leaks above adapter layer.

### Real-runtime integration tests

Run against an actual local Codex installation:

- list real persistent threads;
- read a known thread;
- resume a known thread;
- send a bounded harmless task;
- observe terminal state.

### Controller review

CI success is evidence, not final authorization. Controller independently inspects:

- changed surface;
- permission impact;
- error semantics;
- concurrency/idempotency risk;
- stage boundary compliance.

---

## 13. Delivery Plan / 交付计划

### R0 — Integration Research ✅

Freeze supported integration path and reject speculative assumptions.

### BE-1 — Discovery

Scope:
- official SDK bootstrap;
- `thread_list`;
- internal `ThreadSummary`;
- CLI output;
- unit tests;
- real Windows validation.

### BE-2 — Read Bridge

Scope:
- `read_thread(thread_id)`;
- optional turn/history inclusion;
- normalized read model;
- missing/unavailable thread errors.

No dispatch yet.

### BE-3 — Dispatch

Scope:
- explicit thread targeting;
- resume/attach;
- send one bounded task;
- local task ↔ upstream turn binding;
- duplicate-dispatch protection.

### BE-4 — Status/Event Layer

Scope:
- active turn stream;
- lifecycle normalization;
- completion/failure/interruption/timeout;
- approval-visible state.

### INT-1 — MCP Surface

Scope:
- expose discovery/read/dispatch/status;
- narrow typed schemas;
- deterministic errors;
- external controller demo.

### VAL-1 — End-to-End Controller Loop

Demonstrate:

```text
Controller
→ discover Backend thread
→ read context
→ dispatch bounded task
→ watch execution
→ receive terminal result
```

### REL-0 — v0.1 Pre-alpha

Requirements:
- installation guide;
- supported environment matrix;
- architecture docs;
- threat/permission note;
- known limitations;
- reproducible demo;
- no known P1 defect.

### v0.2 — Evidence Layer

- diff collection;
- validation manifest;
- structured handoff;
- token/context savings measurement.

### v0.3 — Stage-Gate Orchestration

- persistent role mapping;
- controller policies;
- PASS/FIX/BLOCK workflow;
- multi-role routing.

### Future / 非当前承诺

- GUI dashboard;
- remote host control;
- team/multi-user mode;
- GitHub orchestration;
- release automation;
- FlowTracer/Obsidian integration;
- multi-provider support.

---

## 14. Repository Architecture / 仓库结构

Target structure:

```text
Codex-domination/
├── src/codex_domination/
│   ├── runtime.py
│   ├── discovery.py
│   ├── reader.py
│   ├── dispatcher.py
│   ├── status.py
│   ├── events.py
│   ├── models.py
│   ├── errors.py
│   ├── cli.py
│   └── mcp_server.py          # INT-1
├── tests/
│   ├── unit/
│   ├── contract/
│   └── integration/
├── docs/
│   ├── 00-PROJECT-CONTROL.md
│   ├── 01-ARCHITECTURE-v0.1.md
│   ├── 02-R0-INTEGRATION-DECISION.md
│   ├── 10-MASTER-TECHNICAL-DESIGN.md
│   └── stage-specific docs...
├── .github/workflows/
├── pyproject.toml
├── README.md
└── LICENSE
```

The exact file layout may evolve, but module responsibilities must remain explicit.

---

## 15. Documentation Governance / 文档治理

Documentation is part of the engineering contract.

Every implementation stage must produce or update:

1. scope and non-goals;
2. architecture/module changes;
3. external/internal interface changes;
4. test and validation evidence;
5. known risks/limitations;
6. Controller decision and next-stage admission.

Priority order when documents conflict:

```text
00-PROJECT-CONTROL.md
        ↓
10-MASTER-TECHNICAL-DESIGN.md
        ↓
R0 / Architecture Decisions
        ↓
Stage Technical Design
        ↓
Implementation
```

Any intentional deviation must be documented as an architecture decision before merge.

---

## 16. v0.1 Definition of Done / v0.1 完成定义

v0.1 is complete only when an external controller can, through one structured interface:

1. discover persistent Codex threads;
2. read one selected thread;
3. dispatch one bounded task to that exact thread;
4. observe its lifecycle to a deterministic terminal state;
5. receive a structured result/error;
6. do all of the above without UI scraping or manual thread switching;
7. preserve Codex sandbox/approval boundaries;
8. preserve Controller final authority.

That is the first product proof. Everything beyond it is an extension, not a prerequisite.

---

## 17. Current Freeze / 当前冻结结论

As of this baseline:

- official Codex SDK/App Server is the selected execution integration;
- Python is the v0.x bridge implementation language;
- controller-first governance is mandatory;
- MCP is the preferred first external control surface after the local bridge works;
- GUI, GitHub orchestration and broad automation are deferred;
- BE-1 must finish real-runtime validation before merge;
- no later stage may bypass BE-1's gate merely because implementation code exists.

**Next engineering action:** finish BE-1 real-runtime acceptance, then admit BE-2 according to this document.

---

## 18. Architecture Amendment Register / 架构修正案登记

The following architecture amendment is now part of this Master Baseline:

- `docs/13-ARCHITECTURE-AMENDMENT-REPOSITORY-CONTROL.md` — promotes the **Repository Control Plane / Git Orchestrator** to a first-class subsystem for the v0.1→v1.1 evolution while preserving the frozen v0.1 implementation scope.

The current long-range implementation sequence is additionally governed by:

- `docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md`
- `docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md`

Where older text in this Master document says GitHub orchestration is merely an unspecified future capability, these registered documents define the current intended architecture: Git/repository mechanics may become highly automated, but merge/release authority remains explicitly Controller-gated.
