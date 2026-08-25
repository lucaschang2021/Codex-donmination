# Codex Domination — AI Engineering OS Architecture

> Status: **Target Architecture / 目标架构**
>
> Product direction: **Codex-first, not Codex-only.**
>
> Codex Domination is designed as a controller-first operating system for AI software engineering teams. Codex is the first and reference execution runtime. Hermes is the first planned additional agent runtime. Both are governed by the same upper-layer engineering system: roles, stages, evidence, repository control, audit, and explicit Controller authority.

---

## 1. Product Thesis / 产品命题

Codex Domination is not primarily a chatbot manager, a thin multi-agent router, or an autonomous coding swarm.

It is an **AI Software Engineering Control Plane**.

Its job is to turn multiple capable AI agents into a structured engineering organization:

```text
Human / Product Owner
        │
        ▼
Controller
        │
        ▼
Codex Domination
        │
        ├── Project Control
        ├── Role Registry
        ├── Stage Gate Engine
        ├── Task Contract Engine
        ├── Evidence Engine
        ├── Repository Control Plane
        ├── Audit / Policy Layer
        └── Agent Runtime Layer
                 │
                 ├── CodexRuntime
                 ├── HermesRuntime
                 └── FutureRuntime
```

The product principle is:

> **Automate execution, transport, evidence, repetition, repository mechanics and coordination. Preserve explicit judgment and authority.**

中文：

> **自动化执行、传输、证据、重复操作、Git 机械流程和协作；保留明确的判断权与最终授权。**

---

## 2. Why Codex + Hermes / 为什么整合 Codex 与 Hermes

Codex and Hermes are complementary rather than mutually exclusive.

- **Codex** is well suited to persistent coding threads, repository-local engineering, tool execution and software implementation workflows.
- **Hermes** represents a more autonomous agent runtime style: planning, tool use, recovery, broader task execution and potentially stronger research/review autonomy.

Codex Domination does not attempt to replace either runtime.

Instead, it separates two concerns:

### Agency

What an agent runtime can do:

- reason;
- plan;
- use tools;
- modify files;
- execute commands;
- recover;
- continue work;
- produce artifacts.

### Governance

What Codex Domination controls:

- which role owns the task;
- which runtime is assigned;
- what the task boundary is;
- which files/worktree may be touched;
- what evidence is required;
- whether the stage passed;
- whether repository mutation is authorized;
- whether the next stage may start.

The architectural thesis is therefore:

> **Agency without governance becomes chaos. Governance without capable agents becomes bureaucracy. Codex Domination combines both.**

---

## 3. High-Level Architecture / 总体架构

```text
┌──────────────────────────────────────────────────────────┐
│ Human / Product Owner                                    │
└───────────────────────────┬──────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────┐
│ Controller                                               │
│ architecture / review / PASS-FIX-BLOCK / final authority│
└───────────────────────────┬──────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────┐
│ Codex Domination Control Plane                           │
│                                                          │
│  Project Registry                                        │
│  Role Registry                                           │
│  Stage Gate Engine                                       │
│  Task Contract Engine                                    │
│  Context Packager                                        │
│  Evidence Engine                                         │
│  Repository Control Plane                                │
│  Audit / Policy Layer                                    │
│  MCP / CLI / API Control Surface                         │
└───────────────────────────┬──────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────┐
│ Agent Runtime Interface                                  │
│                                                          │
│        CodexRuntime        HermesRuntime       Future     │
└───────────────┬──────────────────┬────────────────────────┘
                ▼                  ▼
        Persistent Codex       Hermes Agents
        engineering roles      autonomous roles
                │                  │
                └──────────┬───────┘
                           ▼
┌──────────────────────────────────────────────────────────┐
│ Repository / Execution Environment                       │
│ Git / Worktrees / Tests / Docker / CI / GitHub          │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Agent Runtime Interface / Agent 运行时接口

The upper control plane must not depend directly on Codex-specific or Hermes-specific internal models.

A normalized logical interface is defined:

```text
AgentRuntime
  discover()
  read_context(agent_id, options)
  attach(agent_id)
  dispatch(agent_id, task_packet)
  watch(execution_id)
  interrupt(execution_id)
  collect_result(execution_id)
  capabilities()
```

### 4.1 discover

Returns explicit runtime identities and minimal metadata.

### 4.2 read_context

Returns a structured historical/context snapshot.

### 4.3 attach

Reattaches to a persistent context when the runtime requires it.

### 4.4 dispatch

Starts one bounded task against one explicit target.

### 4.5 watch

Normalizes runtime-native events into controller-facing lifecycle state.

### 4.6 interrupt

Stops one active execution when supported.

### 4.7 collect_result

Returns terminal result metadata and artifacts.

### 4.8 capabilities

Declares runtime-supported features so the control plane never assumes authority or behavior that is unavailable.

---

## 5. Runtime Implementations / 运行时实现

### 5.1 CodexRuntime — Reference Runtime

Codex remains the first and reference implementation.

Expected mapping:

```text
discover      → thread_list
read_context  → thread/read
attach        → thread_resume
dispatch      → thread.turn / run
watch         → turn stream / runtime events
interrupt     → turn interrupt
collect_result→ terminal turn result
```

Codex-specific concepts such as `thread`, `turn`, App Server and generated SDK models are normalized at the adapter boundary.

### 5.2 HermesRuntime — Planned Second Runtime

Hermes becomes the first planned non-Codex runtime.

Its purpose is not to duplicate Hermes internally. The adapter converts Hermes-native autonomy into Codex Domination's governance contract.

Expected responsibilities:

- register/discover Hermes agents or sessions;
- map Hermes identities into normalized `AgentIdentity`;
- dispatch bounded engineering/research/review tasks;
- normalize execution status;
- preserve Hermes-native recovery/autonomy inside the task boundary;
- collect results/artifacts;
- expose runtime-specific approval/block events where available;
- never inherit merge/release authority automatically.

Before implementation, Hermes integration must undergo its own integration-research gate and ADR-style freeze.

---

## 6. Role Registry / 角色注册表

A role is a governance identity, not a provider identity.

Example:

```yaml
project: FlowTracer
roles:
  controller:
    authority: final

  research:
    runtime: hermes
    agent: research-01

  backend:
    runtime: codex
    agent: codex-thread-backend
    worktree: D:/FlowTracer-wt/backend

  frontend:
    runtime: codex
    agent: codex-thread-frontend
    worktree: D:/FlowTracer-wt/frontend

  security-review:
    runtime: hermes
    agent: security-review-01

  integration:
    runtime: codex
    agent: codex-thread-integration
    worktree: D:/FlowTracer-wt/integration
```

A role definition may include:

- runtime;
- agent identity;
- workspace/worktree;
- allowed paths;
- forbidden actions;
- tool profile;
- evidence requirements;
- stage eligibility;
- escalation policy.

---

## 7. Task Contract Engine / 任务契约引擎

Every worker receives a bounded task packet rather than an open-ended instruction.

Canonical Task Packet:

```text
Project
Version / Stage
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
Failure / Escalation Rules
Developer Report Format
```

The task packet is runtime-independent.

Codex and Hermes may receive different runtime-specific serialization, but they operate under the same engineering contract.

---

## 8. Stage Gate Engine / 阶段门控引擎

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
CLOSED
```

Important invariant:

> Worker agents do not self-admit the next stage.

A worker may report completion, but only the Controller records PASS/FIX/BLOCK and admits the next stage.

---

## 9. Evidence Engine / 证据引擎

Evidence is collected independently of agent prose.

Candidate evidence:

- changed files;
- diff summary;
- test commands and results;
- coverage;
- lint;
- type checks;
- build;
- migrations;
- Docker/service health;
- runtime errors;
- CI status;
- PR state;
- contract deviations;
- runtime execution metadata;
- final worker result.

Target output:

```text
VALIDATION-MANIFEST.md
```

or a structured JSON equivalent.

Principle:

> **Automate evidence, not judgment.**

---

## 10. Repository Control Plane / Git Orchestrator

Git is a first-class subsystem, not an incidental worker capability.

Responsibilities:

- repository inspection;
- branch creation/reuse;
- worktree lifecycle;
- workspace-to-role binding;
- clean-worktree verification;
- commit generation;
- push;
- PR creation/update;
- CI observation;
- merge-authorization validation;
- merge execution;
- post-merge main/worktree synchronization;
- repository audit trail.

### Authority model

Git mechanics may be automated.

Git authority remains explicit.

The ideal flow:

```text
Agent completes bounded task
        ↓
Evidence collected
        ↓
Automatic commit / push / PR
        ↓
CI
        ↓
Controller independent review
        ↓
PASS
        ↓
Merge Authorization bound to exact PR head SHA
        ↓
Repository Control Plane merges
        ↓
Synchronize main + worktrees
        ↓
Next stage admission
```

If the PR head changes after approval, the merge authorization is invalidated.

---

## 11. Project Control / 项目控制

Codex Domination is multi-project by design.

A project profile may contain:

```text
Project Identity
Repository
Default Branch
Worktree Strategy
Role Registry
Runtime Bindings
Current Version
Current Stage
Frozen Architecture Docs
Task Templates
Validation Profile
Repository Policy
Controller Authority Policy
```

This allows the same control plane to manage FlowTracer, Codex Domination itself, Rasputin, or future projects without rebuilding the methodology each time.

---

## 12. Control Surface / 控制面

External operation should converge toward a narrow typed interface exposed through CLI first and MCP/API later.

Candidate high-level tools:

```text
project.list()
project.get_state()
role.list()
role.resolve()
agent.list()
agent.read()
task.dispatch()
task.status()
task.interrupt()
evidence.collect()
stage.get()
stage.review()
stage.approve()
repo.get_state()
repo.prepare_stage()
repo.open_pr()
repo.get_ci()
repo.merge_authorized()
```

The control surface must never expose an unrestricted shell merely for convenience.

---

## 13. Natural-Language Controller Experience / 最终交互体验

The long-term interface should hide mechanical complexity.

Example:

```text
User:
FlowTracer, continue.

Controller:
Current stage: BE-7.
Backend role resolved to CodexRuntime / exact thread ID.
Stage contract loaded.
Worktree prepared.
Implementation task dispatched.
Execution completed.
82 tests passed.
CI passed.
1 P2 issue detected during Controller review.
Repair task dispatched to same Backend role.
Second validation passed.
Awaiting final merge authorization.
```

The user should think in projects, versions, stages and decisions — not in Git commands, thread switching and repetitive copy/paste.

---

## 14. Failure Taxonomy / 故障分类

### F1 — Implementation Defect

Example: parser bug, wrong field mapping, missing validation.

Action: fix inside the current stage.

### F2 — Runtime / Compatibility Defect

Example: Codex SDK drift, Hermes integration behavior, Windows process lifecycle.

Action: repair the runtime adapter/compatibility layer while preserving upper contracts.

### F3 — Contract Defect

Example: unsafe retry semantics, ambiguous execution status, repository authorization ambiguity.

Action: Controller revises the affected contract before implementation continues.

### F4 — Architecture Invalidated

Example: an assumed supported runtime primitive fundamentally cannot satisfy the required capability.

Action: stop the stage, issue an ADR, update architecture, then resume.

---

## 15. Security & Authority / 安全与权限

1. Never bypass runtime authentication, sandboxing or approval models.
2. Every task targets a concrete role and runtime identity.
3. Every repository mutation targets an explicit repository state.
4. Cross-runtime handoffs use structured task/evidence packets.
5. Secrets are isolated by project/runtime/role boundaries.
6. No worker runtime silently obtains merge/release authority.
7. Controller PASS is distinct from worker completion.
8. Merge authorization is state-bound and revocable by repository change.
9. Destructive operations require explicit policy and audit records.
10. Runtime/provider choice must never make control-critical routing ambiguous.

---

## 16. Version Evolution / v0.1 → v1.1

### v0.1 — Codex Discovery Foundation

- Codex runtime bootstrap;
- persistent thread discovery;
- normalized identities;
- CLI.

### v0.2 — Thread Read

- structured history/context read.

### v0.3 — Resume / Attachment

- deterministic reattachment to persistent Codex contexts.

### v0.4 — Bounded Dispatch

- one explicit bounded task to one explicit role/thread.

### v0.5 — Status

- normalized execution lifecycle.

### v0.6 — Evidence

- validation manifests and mechanical evidence.

### v0.7 — Role Registry

- stable engineering roles and project bindings.

### v0.8 — Stage Gate

- executable Controller-first methodology.

### v0.9 — MCP Control Surface

- structured external Controller integration.

### v1.0 — Codex Engineering Control Plane

- complete Codex-first end-to-end engineering workflow.

### v1.1 — AI Engineering OS Expansion

- Repository Control Plane;
- workflow automation;
- reusable project/stage/task templates;
- automatic repair loops;
- runtime abstraction hardening;
- Hermes integration research and adapter admission;
- multi-runtime role binding;
- workflow efficiency metrics.

The roadmap remains Codex-first: Hermes support expands the proven control plane rather than delaying the initial Codex proof.

---

## 17. Happy-Path End State / 理想终局

```text
Product requirement
        ↓
Controller freezes architecture
        ↓
Stage Gate admits work
        ↓
Role Registry resolves worker
        ↓
Agent Runtime chosen explicitly
   ┌────┴─────┐
   ▼          ▼
 Codex      Hermes
   └────┬─────┘
        ↓
Bounded task execution
        ↓
Evidence Engine
        ↓
Repository Control Plane
        ↓
PR + CI
        ↓
Controller independent review
   ┌────┼─────┐
   ▼    ▼     ▼
 PASS  FIX  BLOCK
   │    │
   │    └──→ same role/runtime repair loop
   ▼
Merge Authorization
        ↓
Automated merge + sync
        ↓
Next stage
```

---

## 18. Product Positioning / 产品定位

Short version:

> **Codex Domination is a controller-first operating system for AI software engineering teams.**

More precise version:

> **Codex-first, multi-runtime engineering governance: persistent agents, bounded tasks, evidence, stage gates, Git control and explicit human authority.**

Chinese:

> **Codex Domination 是一套以总控为核心的 AI 软件工程操作系统：Codex 优先、可扩展多 Agent Runtime，用 Stage Gate、证据、Git 控制和明确授权把 AI Agent 组织成真正的软件工程团队。**

---

## 19. Non-goals / 非目标

Even in the expanded architecture, Codex Domination is not intended to become:

- an unrestricted general autonomous-agent swarm;
- a generic consumer chatbot platform;
- a replacement for Codex or Hermes;
- a system that bypasses runtime security boundaries;
- a product that equates worker completion with production authorization;
- an excuse to automate architectural judgment away.

The system automates the engineering machine around judgment while keeping judgment explicit.
