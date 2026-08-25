# Codex Domination

> **A controller-first operating system for AI software engineering teams.**  
> **面向 AI 软件工程团队的总控优先开发操作系统。**

Codex Domination is an experimental AI engineering control plane that turns persistent coding agents into a structured software team.

It is **Codex-first, not Codex-only**: OpenAI Codex is the first and reference runtime, while Hermes is the first planned additional agent runtime. The upper engineering system — roles, bounded tasks, evidence, stage gates, repository control, audit and final authority — remains independent from any single agent runtime.

Codex Domination 是一套实验性的 AI 软件工程控制平面，它把多个长期存在的 AI Agent 组织成结构化的软件开发团队。

项目坚持 **Codex-first, not Codex-only**：OpenAI Codex 是第一个、也是基准 Agent Runtime；Hermes 是首个计划接入的第二运行时。上层的角色、任务契约、证据、Stage Gate、Git 控制、审计与最终授权不绑定单一 Agent。

> [!IMPORTANT]
> The repository is still **pre-alpha**. The architecture intentionally describes the target system ahead of implementation. The immediate engineering path remains narrow: prove the Codex control loop first, then expand the proven control plane.
>
> 本仓库仍处于 **Pre-alpha**。架构文档会先于实现描述终局系统，但实际开发仍按窄范围逐阶段推进：先验证 Codex 控制闭环，再扩展已经被证明可靠的控制平面。

---

## The idea / 核心想法

Today, advanced AI-assisted development often looks like this:

```text
Human
 ├── opens Backend agent
 ├── copies task
 ├── waits
 ├── copies result
 ├── checks Git
 ├── checks tests
 ├── opens Integration agent
 ├── repeats context
 └── manually decides what happens next
```

The individual agents may be powerful, but the **engineering organization around them is still manual**.

Codex Domination moves that coordination into a control plane:

```text
                         Human / Product Owner
                                  │
                                  ▼
                         Controller / 总控
                                  │
                                  ▼
┌──────────────────────────────────────────────────────┐
│                 Codex Domination                     │
│                                                      │
│ Project Control  • Role Registry  • Stage Gate       │
│ Task Contracts   • Evidence       • Git Control      │
│ Audit / Policy   • MCP / CLI      • Runtime Routing  │
└───────────────────────────┬──────────────────────────┘
                            │
                    Agent Runtime Layer
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
             Codex                   Hermes
       persistent coding       autonomous agent roles
                            │
                            ▼
               Git / Worktrees / CI / GitHub
```

The Controller spends its reasoning budget on architecture, review, risk and decisions — not on mechanical relay.

总控把推理预算花在架构、审查、风险与决策上，而不是不停复制粘贴、切窗口和手工操作 Git。

---

## Product philosophy / 产品哲学

### Agency + Governance

Agent runtimes provide **agency**:

- reasoning;
- planning;
- tool use;
- coding;
- execution;
- recovery;
- artifact generation.

Codex Domination provides **governance**:

- which role owns the work;
- which runtime executes it;
- what the task boundary is;
- what workspace may be modified;
- what evidence is required;
- whether the stage passed;
- whether a merge is authorized;
- whether the next stage may start.

> **Agency without governance becomes chaos. Governance without capable agents becomes bureaucracy.**

---

## What it eventually does / 最终功能

### 1. Persistent Agent Runtime Control

Discover, read, resume, dispatch and observe long-lived agent contexts.

Reference runtime:

```text
CodexRuntime
  discover      → persistent Codex threads
  read_context  → structured thread history
  attach        → resume persistent thread
  dispatch      → bounded turn/task
  watch         → execution events/status
  interrupt     → stop active execution
  result        → terminal result
```

Planned expansion:

```text
AgentRuntime
├── CodexRuntime      # reference implementation
├── HermesRuntime     # planned second runtime
└── FutureRuntime     # later, explicit admission only
```

### 2. Role Registry

A persistent agent becomes an engineering role instead of an anonymous chat.

```text
Controller
Backend
Frontend
Integration
Research
Security Review
GitHub / Release
```

Each role may bind:

```text
runtime
agent/thread ID
project
workspace/worktree
allowed paths
forbidden actions
validation profile
stage eligibility
```

A role is a governance identity, not a model/provider identity.

### 3. Bounded Task Contracts

Agents receive structured work packages rather than vague open-ended prompts.

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

### 4. Execution Status

The system observes actual lifecycle state rather than trusting a worker saying “done”.

```text
UNKNOWN
ACCEPTED
RUNNING
WAITING_APPROVAL
BLOCKED
COMPLETED
FAILED
INTERRUPTED
TIMED_OUT
```

### 5. Evidence Engine

Mechanical validation is collected automatically:

```text
git diff
changed files
tests
coverage
lint
type checks
build
migrations
Docker/service health
runtime errors
CI
PR state
contract deviations
```

Target artifact:

```text
VALIDATION-MANIFEST.md
```

> **Automate evidence, not judgment.**

### 6. Stage Gate Engine

The engineering methodology itself becomes executable state.

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

A developer/worker agent may report completion, but it does **not** admit the next stage.

Only the Controller records `PASS / FIX / BLOCK`.

### 7. Repository Control Plane / Git Orchestrator

Git becomes a first-class subsystem instead of a manual chore.

Codex Domination is designed to eventually manage:

```text
repository inspection
branch creation / reuse
worktree lifecycle
workspace-role binding
clean-worktree checks
commit
push
PR creation / update
CI observation
merge authorization
merge
post-merge synchronization
```

The intended workflow:

```text
Agent finishes task
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
Automatic merge
      ↓
Synchronize main + worktrees
      ↓
Next stage
```

If code changes after approval, the old merge authorization becomes invalid.

**Git mechanics may be automated. Git authority remains explicit.**

### 8. Multi-Project Control

One control plane can eventually govern several real projects.

```text
FlowTracer
Codex Domination
Rasputin
future projects
```

Each project may define its own:

```text
repository
roles
runtime bindings
worktree strategy
architecture docs
current version/stage
task templates
validation profile
Git policy
Controller authority
```

### 9. MCP / Structured Control Surface

The system is intended to expose a narrow structured interface so an external Controller such as ChatGPT can operate it.

Candidate surface:

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
repo.get_state()
repo.open_pr()
repo.get_ci()
repo.merge_authorized()
```

No unrestricted shell is exposed merely for convenience.

---

## Codex + Hermes / Codex 与 Hermes 如何整合

Codex Domination does not try to merge Codex and Hermes into one giant agent implementation.

Instead, both plug into one governance system:

```text
                         Controller
                             │
                        Stage Gate
                             │
                      Role Resolution
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
            Backend Role         Research Role
             CodexRuntime         HermesRuntime
                  │                     │
                  └──────────┬──────────┘
                             ▼
                       Evidence Engine
                             │
                     Repository Control
                             │
                          PR / CI
                             │
                    Controller Review
```

Example project profile:

```yaml
roles:
  research:
    runtime: hermes
    agent: research-01

  backend:
    runtime: codex
    agent: codex-thread-backend

  frontend:
    runtime: codex
    agent: codex-thread-frontend

  security-review:
    runtime: hermes
    agent: security-review-01

  integration:
    runtime: codex
    agent: codex-thread-integration
```

Hermes is a **planned integration**, not a currently implemented dependency. Before implementation, its supported integration surface must pass a dedicated research/ADR gate.

Hermes 是**计划整合项**，不是当前已经实现的依赖。真正接入之前必须先完成独立的集成面研究和 ADR 冻结。

---

## The ideal experience / 理想体验

The long-term user experience should be extremely simple.

```text
You:
FlowTracer, continue.

Controller:
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
```

The user thinks in:

```text
project
architecture
stage
risk
decision
```

—not in:

```text
thread switching
copy/paste
git branch
git worktree
git commit
git push
PR boilerplate
repeated status checks
```

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
| **v1.1** | workflow automation + Repository Control + multi-runtime expansion + Hermes integration path |

The project remains **Codex-first** during implementation. Multi-runtime support expands a proven system; it does not delay the first reliable product proof.

---

## Failure model / 故障模型

Real implementation failures are classified before architecture is changed.

### F1 — Implementation defect

Fix inside the current stage.

### F2 — Runtime / compatibility defect

Fix the Codex/Hermes/runtime adapter or compatibility layer.

### F3 — Contract defect

Controller updates the affected technical contract before work continues.

### F4 — Architecture invalidated

Stop the stage, issue an ADR, change the architecture explicitly, then resume.

This lets the project model the ideal successful workflow first without pretending real implementation will be bug-free.

---

## Project principles / 项目原则

1. **Controller first.** / 总控优先。
2. **Codex-first, not Codex-only.** / Codex 优先，但不锁死 Codex。
3. **Persistent agents over disposable prompts.** / 优先长期 Agent。
4. **Roles over anonymous conversations.** / 用工程角色管理 Agent。
5. **Bounded tasks over vague autonomy.** / 任务必须有边界。
6. **Structured state over repeated summaries.** / 优先结构化状态。
7. **Automate evidence, not judgment.** / 自动化证据，不自动化判断。
8. **Automate Git mechanics, preserve Git authority.** / 自动化 Git 操作，保留 Git 授权。
9. **Exact targeting for control-critical actions.** / 控制关键操作必须精确定位。
10. **Architecture changes require explicit decisions.** / 架构变化必须留下明确决策。

---

## Documentation / 技术文档

The architecture is documented before heavy implementation so Codex can later execute bounded work packages rather than redesigning the system during coding.

Key documents:

- [`docs/00-PROJECT-CONTROL.md`](./docs/00-PROJECT-CONTROL.md) — governance baseline
- [`docs/02-R0-INTEGRATION-DECISION.md`](./docs/02-R0-INTEGRATION-DECISION.md) — official Codex integration decision
- [`docs/10-MASTER-TECHNICAL-DESIGN.md`](./docs/10-MASTER-TECHNICAL-DESIGN.md) — master technical baseline
- [`docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md`](./docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md) — staged roadmap
- [`docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md`](./docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md) — repository control architecture
- [`docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md`](./docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md) — unified Codex + Hermes + Git + Stage Gate target architecture

Documentation authority remains explicit; stage implementation must not silently contradict frozen architecture.

---

## Current status / 当前状态

**Pre-alpha / architecture-first implementation.**

Current practical priority:

```text
Codex v0.1
→ discover real persistent threads
→ validate on a real local Codex environment
→ Controller gate
→ continue to read / resume / dispatch / status
```

Hermes, Repository Control and broader AI Engineering OS capabilities are part of the documented target architecture, but they do not bypass the stage-gated Codex foundation.

---

## Long-term positioning / 长期定位

Short version:

> **Operating system for AI software engineering teams.**

More precise:

> **Codex-first, multi-runtime engineering governance: persistent agents, bounded tasks, evidence, stage gates, Git control and explicit human authority.**

中文：

> **Codex Domination 是一套以总控为核心的 AI 软件工程操作系统：Codex 优先、可扩展 Hermes 等 Agent Runtime，用角色、任务契约、Stage Gate、证据与 Git 控制，把 AI Agent 组织成真正的软件工程团队。**

---

## License

MIT License. See [`LICENSE`](./LICENSE).
