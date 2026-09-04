# Möbius — 中文文档

**面向 AI 软件工程的 Architecture & Development Governance Control Plane（架构与开发治理控制平面）。**

Möbius 负责治理 Codex、Claude Code、Astra、Hermes 及未来 Coding Agent 如何规划、修改、验证、审查并持续演化复杂软件系统，避免开发速度提升的同时，架构边界、测试契约与权限体系被悄然破坏。

[English](README.md) · [总架构](docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md) · [架构契约](docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md) · [路线图](ROADMAP.md) · [MIT](LICENSE)

> **当前状态：** Pre-alpha / Architecture-first。当前实现仍然 Codex-first，但 Codex 现在被定义为第一条“受治理的执行 Runtime”，而不是 Möbius 产品本身的定义。

## 为什么需要 Möbius？

AI Coding Agent 已经越来越会写代码。真正困难的问题正在变成：

- 如何防止一个 Service 在持续迭代中变成 God Module？
- 如何防止 REST/MCP/UI Adapter 逐渐吞掉 Application Kernel？
- 如何在隐藏依赖、全局状态、Import Side Effect、初始化顺序耦合扩散之前发现它们？
- 如何保证 Domain Decision 不被塞进 Orchestration Service？
- 如何在增加 Provider、Agent、Framework、数据库和外部集成后仍然保持独立测试能力？
- 如何把审查与 Merge Authority 绑定到精确的仓库状态？

Möbius 就是把这些架构意图转化为**可执行、可审计、可版本化的软件工程治理**。

> **Agent 执行，Git 记录，测试验证行为，Architecture Contract 约束演化，Evidence 支撑审查，Möbius 治理 Change。**

## 核心对象：Change

Möbius 不再把“Agent”作为核心对象，而把一次工程 **Change** 作为核心治理对象。

一个 Change 可以包含：

- Objective / Non-goals
- Repository / Branch / Worktree
- Role / Runtime
- Architecture Contract Snapshot
- Allowed / Forbidden Dependency
- Allowed Files / Permission Boundary
- Implementation Plan
- Execution Evidence
- Architecture Diff
- Tests / CI / Build Evidence
- Review Findings
- PASS / FIX / BLOCK
- Merge Authorization

这个 Change 可以由一个 Agent、多个 Agent、人类开发者或混合团队执行。

## 六大平面

| 平面 | 职责 |
|---|---|
| **Governance** | Controller Authority、Stage Gate、Change Contract、Risk Policy、PASS/FIX/BLOCK、精确 SHA Merge Authorization |
| **Architecture** | Architecture Contract、模块职责、依赖方向、Side-effect Policy、State Ownership、复杂度门禁、Architecture Drift |
| **Runtime** | Codex 优先；Claude Code / Astra / Hermes / Future Runtime 通过统一 Adapter 接入 |
| **Evidence** | Diff、Test、CI、依赖图变化、Architecture Finding、Validation Manifest |
| **Repository** | Branch/Worktree、Commit、PR、CI、Reviewed-head Binding、Merge Mechanics |
| **Knowledge** | ADR、架构债历史、失败与修复、Runtime 兼容性、工程知识、Obsidian Projection |

```text
                         Human / Controller
                                  |
                                  v
+----------------------------------------------------------------+
|                             MÖBIUS                             |
|                                                                |
| Governance | Architecture | Runtime | Evidence | Repo | Memory |
+-------------+--------------+---------+----------+------+--------+
                |                |          |        |
                |                |          |        +--> Git / PR / CI
                |                |          +--> tests / diff / architecture facts
                |                +--> Codex / Claude Code / Astra / Hermes
                +--> policy / gate / merge authority
```

## Architecture Contract

每个被 Möbius 治理的项目都可以声明自己的版本化 Architecture Contract。

例如：

```yaml
schema_version: 1
project: FlowTracer

layers:
  api:
    may_depend_on: [application, schemas]
  application:
    may_depend_on: [domain, ports]
    forbidden: [fastapi, electron]
  domain:
    filesystem: forbidden
    network: forbidden
    environment_access: forbidden

mutable_state:
  module_globals: forbidden

required_checks:
  - unit_tests
  - contract_tests
  - architecture_gate
```

Möbius **不会强迫所有项目使用同一种 Clean Architecture**。它治理的是项目自己明确声明的架构，而不是把一种架构教条强加给所有仓库。

详细规范见 [`docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md`](docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md)。

## Architecture Gate

在 Merge Authorization 之前，Möbius 可以检查：

- Forbidden Dependency Direction
- Cross-layer Import
- Module Responsibility Leakage
- 新增 Global Mutable State
- Import-time Filesystem / Network / Plugin Side Effect
- Public Interface Change
- Architecture Contract Deviation
- File / Dependency Complexity Growth
- Fake / In-memory Adapter 是否被破坏
- Test Isolation / Failure Isolation 是否退化

测试全部通过只能说明：**被测试的行为通过了**。它不能自动证明架构仍然健康。

示例：

```yaml
architecture_gate:
  status: FIX
  findings:
    - severity: P1
      rule: adapter_must_not_depend_on_entrypoint
      evidence: "REST adapter imports MCP entrypoint as business service"
      remediation: "extract application service and inject both adapters"
```

## 受治理的开发生命周期

```text
REQUEST
  ↓
CONTEXT LOAD
  ↓
ARCHITECTURE CONTRACT SNAPSHOT
  ↓
PLAN
  ↓
PLAN GATE
  ↓
EXECUTION
  ↓
TEST / BUILD / CI EVIDENCE
  ↓
ARCHITECTURE DIFF
  ↓
INDEPENDENT REVIEW
  ↓
PASS / FIX / BLOCK
  ↓
MERGE AUTHORIZATION
  ↓
MERGE
  ↓
KNOWLEDGE EXTRACTION
```

Plan Gate 的意义是：**在 Agent 花大量时间执行之前，就先发现计划本身违反架构。**

Architecture Diff 则关注：一次 Change 之后，整个仓库的依赖、状态、接口、副作用和复杂度结构发生了什么变化。

## Multi-Agent 降级为 Execution Strategy

Möbius 可以编排多个 Agent，但这不是产品核心护城河。

```text
                  Möbius Governance
                         |
              +----------+----------+
              |                     |
        Architecture Gate      Evidence Gate
              |                     |
              +----------+----------+
                         |
                  Execution Strategy
                         |
          +--------------+--------------+
          |              |              |
        Codex        Claude Code       Astra
```

一个单 Agent Change 和一个多 Agent Change 使用同一份 Architecture Contract 与治理规则。

## Controller-first Authority

可以高度自动化：

- Repository Inspection
- Worktree 准备
- Dependency Graph 提取
- Test / Lint / Type / Build
- Architecture Rule Evaluation
- Evidence Collection
- PR Metadata
- Knowledge Projection

必须保留显式 Policy / Controller 权限：

- Architecture Redesign
- Security Risk Acceptance
- Contract Weakening
- Destructive Migration Approval
- Merge Authorization
- Release Authority

> **自动化 Evidence 与机械动作；保留架构、风险与最终权限。**

## Runtime Strategy

Möbius 继续坚持 **Codex-first, not Codex-only**：

```text
EngineeringRuntime
├── CodexRuntime
├── ClaudeCodeRuntime
├── AstraRuntime
├── HermesRuntime
└── FutureRuntime
```

原有 Persistent Codex Control Bridge 不会被废弃，而是成为 Möbius 第一条受治理执行链。

## 三个真实治理样本

### FinTerminal

Möbius 应能够发现或阻止：

- REST Adapter 依赖 MCP EntryPoint 形成 Giant Application Kernel
- Import-time Plugin Loading
- Config / Runtime State 藏在 Module Global
- 核心逻辑必须完整启动 MCP/FastAPI/Electron 才能测试

### FlowTracer

Möbius 应保护：

- `main.py` 保持 Bootstrap-only
- Explicit Dependency Injection
- Provider Abstraction + Fake Provider
- Service / Provider Boundary
- acquisition / intelligence 逐渐长成 God Service 时提前报警

### Gallop

Möbius 应保护：

- Deterministic Evidence / Mastery / Progression Engine
- Event Journal Authority
- Domain Decision 不进入 Orchestration Service
- Progressive Mentorship Logic 进入独立 Deterministic Engine，而不是不断堆入 `Automation`

## 与 Rasputin 的边界

```text
Rasputin
= AI Runtime Sovereign Control / Policy / Authority /
  Computational Capital / Verification / Audit / Trust

Möbius
= Development-time Architecture & Engineering Change Governance
```

两者未来可以集成，但 Möbius 必须能够作为独立开发者工具运行。

## 路线图

| 阶段 | 核心目标 |
|---|---|
| **A — Contract MVP** | Architecture Contract、Repo Scanner、Module/Dependency Map、Baseline Architecture Gate |
| **B — Codex Governed Execution** | Persistent Runtime + Change Contract + Plan Gate + Evidence |
| **C — Architecture Diff** | Dependency / State / Side-effect / Interface / Complexity Delta |
| **D — Repository Governance** | Worktree / PR / CI / Exact-SHA Merge Authorization |
| **E — Multi-runtime** | Claude Code / Astra / Hermes Adapter |
| **F — Knowledge** | ADR、Architecture Debt、工程记忆、Obsidian Projection |

详细版本路线见 [`ROADMAP.md`](ROADMAP.md)。

## 永久设计原则

1. **Govern Change, Not Intelligence.**
2. Architecture 尽可能成为 Executable Policy。
3. Execution 永远不自动等于 Authority。
4. Evidence 永远不静默替代 Judgment。
5. Runtime 不拥有 Product Architecture。
6. Adapter 不得成为 Application Kernel。
7. Domain Decision 应进入 Deterministic Domain/Application Engine，而不是 Transport Entrypoint。
8. Global Mutable State 必须有明确 Owner 与 Lifecycle。
9. Import-time Side Effect 属于例外，必须显式声明。
10. Architecture Contract 必须版本化、可审查。
11. Architecture Drift 必须在变成 Architecture Collapse 前可见。
12. Möbius 最终必须使用自己的规则治理 Möbius 自己。

## 技术文档

- [`docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md`](docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md) — **当前权威产品总架构**
- [`docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md`](docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md) — **架构契约与 Architecture Gate 规范**
- [`docs/00-PROJECT-CONTROL.md`](docs/00-PROJECT-CONTROL.md) — 历史 Codex-first Project Control 基线
- [`docs/02-R0-INTEGRATION-DECISION.md`](docs/02-R0-INTEGRATION-DECISION.md) — Codex 集成决策
- [`docs/10-MASTER-TECHNICAL-DESIGN.md`](docs/10-MASTER-TECHNICAL-DESIGN.md) — CodexRuntime 早期技术实现基线

正式产品名：**Möbius / 莫比乌斯**。  
历史代号：**Codex Domination**。

## License

Möbius 使用 [MIT License](LICENSE)。
