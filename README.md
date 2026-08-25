# Codex Domination

> **Control multiple persistent Codex agents from one controller.**  
> **由一个总控统一读取、调度并监督多个持久化 Codex Agent。**

Codex Domination is an experimental orchestration bridge for multi-agent Codex workflows. It is designed for developers who use several long-lived Codex threads as specialized engineering roles and want a single controller to understand their conversations, dispatch tasks, inspect status, and coordinate handoffs.

Codex Domination 是一个面向多 Codex Agent 工作流的实验性编排桥。它服务于这样一种开发方式：多个长期存在的 Codex 对话分别承担后端、前端、集成、发布等角色，而一个总控能够统一读取对话、派发任务、查看状态并完成角色间交接。

> [!IMPORTANT]
> This repository is an early-stage project definition. The first objective is a narrow, verifiable v0.1 — not a full autonomous software-development platform.
>
> 本仓库目前处于早期项目定义阶段。第一目标是完成一个狭窄、可验证的 v0.1，而不是立即构建完整的自主软件开发平台。

## Why / 为什么

Today, multi-Codex workflows often require a human to manually switch between threads, copy task instructions, summarize completion reports, check execution state, and relay results back to a controller. That works, but it creates duplicated context, token overhead, and coordination friction.

目前，多 Codex 工作流往往仍依赖人工在不同对话之间切换：复制任务、转交结果、总结执行情况、检查状态，再把信息传回总控。这种方式可以工作，但会产生大量重复上下文、额外 token 消耗和协调成本。

Codex Domination aims to turn that manual relay layer into a structured bridge:

Codex Domination 的目标，是把这层人工中转变成结构化桥接层：

```text
                    Controller / 总控
                           │
                           ▼
                  Codex Domination
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
      Backend          Frontend        Integration
      后端 Agent        前端 Agent        集成 Agent
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    Release / GitHub
                     发布 / GitHub
```

The controller should spend its reasoning budget on architecture, review, risk and decisions — not on repeatedly reconstructing mechanical execution evidence.

总控应该把推理预算花在架构、审查、风险和决策上，而不是反复重建机械性的执行证据。

## v0.1 — The smallest useful bridge / 最小可用桥

The first release deliberately targets only four capabilities:

第一版刻意只解决四件事：

- **`list_threads`** — discover available persistent Codex threads / 列出可用的持久化 Codex 对话
- **`read_thread`** — read structured conversation and execution history / 读取结构化对话与执行历史
- **`send_task`** — dispatch an instruction to a selected Codex thread / 向指定 Codex 对话派发任务
- **`watch_status`** — observe task/thread state and completion signals / 观察任务与对话状态及完成信号

A future MCP-facing interface may expose a small surface such as:

未来可通过 MCP 暴露极小的接口面，例如：

```text
codex.list_threads()
codex.read_thread(thread_id)
codex.send_task(thread_id, prompt)
codex.get_status(thread_id)
```

The exact API is **not frozen yet**. The goal of v0.1 is to validate the control loop first.

具体 API **尚未冻结**。v0.1 首先验证的是控制闭环本身。

## Core design / 核心设计

### 1. Conversation Read / 对话读取

Read useful structured state instead of scraping the UI whenever possible:

尽可能读取结构化状态，而不是依赖 UI 抓取：

```text
threads
messages
agent responses
tool calls
approvals
diffs
execution state
```

### 2. Task Dispatch / 任务派发

A controller should be able to select a persistent Codex role and send a task without manual copy/paste.

总控应当能够直接选择一个长期存在的 Codex 角色并派发任务，而不需要人工复制粘贴。

```text
Controller
   ├──> Backend
   ├──> Frontend
   ├──> Integration
   └──> Release
```

### 3. Structured Handoff / 结构化交接

Developer agents should not need to spend large amounts of context rewriting what machines can already collect.

开发 Agent 不应该再消耗大量上下文，重复描述机器本来就能自动收集的信息。

A handoff can eventually contain:

未来的交接信息可包括：

```yaml
task: BE-4
status: completed
changed_files: 11
tests: 82 passed
branch: feat/be-4
needs_controller_review: true
```

### 4. Controller-first governance / 总控优先治理

Codex Domination is **not** intended to remove the controller. Mechanical evidence can be automated; independent reasoning and review should remain explicit.

Codex Domination **不是**为了消灭总控。机械证据可以自动化，但独立推理、复核与准入决策仍应被明确保留。

A target stage-gate loop:

目标 Stage Gate 流程：

```text
Controller admits stage
        ↓
Developer agent executes
        ↓
Bridge collects evidence
        ↓
Controller reviews risk + diff + validation
        ↓
PASS / FIX / BLOCK
        ↓
Merge / next stage
```

## Architecture direction / 架构方向

The preferred direction is a proper execution-layer integration rather than screen automation:

优先路线是执行层集成，而不是屏幕自动化：

```text
Codex App Server / Codex SDK / supported hooks
                    │
                    ▼
            Codex Domination Bridge
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
       MCP       Event Store   Validation
                    │
                    ▼
                Controller
```

Potential internal modules:

潜在内部模块：

```text
src/
├── app_server_client.*
├── thread_manager.*
├── task_dispatcher.*
├── event_store.*
├── status_watcher.*
└── mcp_server.*
```

Implementation language and protocol details will be selected only after validating the current Codex integration surface.

具体实现语言与协议细节将在验证当前 Codex 可用集成接口后再冻结。

## Non-goals for v0.1 / v0.1 明确不做

To keep the first release fast and defensible, v0.1 will **not** attempt to build:

为了让首版足够快、足够清晰，v0.1 **不会**尝试构建：

- a full DevOS / 完整 DevOS
- a large graphical dashboard / 大型图形化控制台
- Obsidian or knowledge-base integration / Obsidian 或知识库集成
- GitHub PR orchestration / GitHub PR 全自动编排
- autonomous merge decisions / 自主合并决策
- general-purpose multi-model agent framework / 通用多模型 Agent 框架
- UI scraping as the primary architecture / 以 UI 抓取作为核心架构

## Roadmap / 路线图

### v0.1 — Bridge
- [ ] Validate the supported Codex integration surface / 验证 Codex 可用集成接口
- [ ] List persistent threads / 列出持久化对话
- [ ] Read a selected thread / 读取指定对话
- [ ] Send a task to a selected thread / 向指定对话派发任务
- [ ] Observe task status / 获取任务状态
- [ ] Provide a minimal MCP-compatible control surface / 提供最小 MCP 控制面

### v0.2 — Evidence
- [ ] Structured task events / 结构化任务事件
- [ ] Diff and validation evidence / Diff 与验证证据
- [ ] Machine-generated handoff manifest / 自动生成交接清单
- [ ] Token/context reduction experiments / Token 与上下文节省实验

### v0.3 — Orchestration
- [ ] Controller-driven stage gates / 总控驱动 Stage Gate
- [ ] Role routing / 角色路由
- [ ] Failure/retry semantics / 失败与重试语义
- [ ] Multi-project coordination experiments / 多项目协调实验

See [`ROADMAP.md`](./ROADMAP.md) for the project boundary and milestone definitions.

完整项目边界和里程碑定义见 [`ROADMAP.md`](./ROADMAP.md)。

## Project principles / 项目原则

1. **Persistent agents over disposable prompts.** / 优先长期 Agent，而不是一次性 Prompt。
2. **Structured state over repeated summaries.** / 优先结构化状态，而不是重复总结。
3. **Automate evidence, not judgment.** / 自动化证据，不自动化判断。
4. **Controller remains the final gate.** / 总控保留最终准入权。
5. **Small surface before large platform.** / 先做小而稳的接口，再谈大平台。
6. **No UI scraping unless there is no supported integration path.** / 除非没有受支持的集成路径，否则不依赖 UI 抓取。

## Status / 当前状态

**Project definition / Pre-alpha.** No production-ready implementation exists yet.

**项目定义阶段 / Pre-alpha。** 当前尚无可用于生产环境的实现。

The immediate objective is to prove one end-to-end loop:

当前唯一最高优先级，是证明一个完整闭环：

```text
Controller
  → discover Codex thread
  → read thread
  → dispatch task
  → observe completion
  → receive structured evidence
```

Once that loop works reliably, the project can grow from a bridge into a true Codex orchestration layer.

只有当这条链路稳定成立之后，项目才会从“桥”继续成长为真正的 Codex 编排层。

## License / 许可证

MIT License. See [`LICENSE`](./LICENSE).
