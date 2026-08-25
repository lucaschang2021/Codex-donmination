# Möbius — 中文文档

**以 Controller 为核心的 AI 软件工程团队操作系统：统一持久化 Agent Runtime、阶段治理、可验证证据、Git 仓库自动化与长期知识记忆。**

[English](README.md) · [总架构](docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md) · [版本路线](docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md) · [知识 / Obsidian](docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md) · [Git Orchestrator](docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md) · [MIT](LICENSE)

> **当前状态：** Möbius 目前处于 Pre-alpha / Architecture-first 阶段。我们刻意先冻结完整目标架构，再逐阶段实现。当前最高工程优先级仍是验证真实、可靠的 Codex 控制闭环。

## 为什么需要 Möbius？

AI Coding Agent 已经能够编写、测试、检查和修改软件。真正困难的问题正在从“AI 会不会写代码”转向“如何把多个长期存在的 Agent 组织成一个有纪律、可验证、可治理的软件工程团队”。

这意味着系统需要知道：谁可以做什么、当前处于哪个工程阶段、哪些文件允许修改、任务是否真的完成、Git 当前处于什么状态、谁有权批准合并，以及这支 AI 工程团队在开发过程中学到了什么。

Möbius 就是把这一层工程协调与治理变成基础设施。

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**  
> **Agent 执行，Git 记录，Evidence 证明，Obsidian 记忆，Möbius 治理。**

Möbius 坚持 **Codex-first, not Codex-only**。OpenAI Codex 是第一个参考 Runtime；Hermes 是计划接入的第二 Runtime；未来其他 Agent Runtime 可以通过稳定的 Adapter 边界加入，而不需要重写上层工程治理体系。

## 五大控制平面

| 平面 | 职责 |
|---|---|
| Governance / 治理 | Project Control、Role Registry、Bounded Task Contract、Stage Gate、Policy、Controller 最终权限 |
| Runtime / 执行 | CodexRuntime 优先；HermesRuntime 计划接入；未来 Runtime 通过统一 Adapter 接入 |
| Evidence / 证据 | 执行状态、Diff、测试、Validation Manifest、CI 事实、审计证据 |
| Repository / 仓库 | Git/worktree、commit、push、PR、CI、精确状态 Merge Authorization、合并后同步 |
| Knowledge / 知识 | 结构化工程记忆，以及面向人的 Obsidian Knowledge Projection |

```text
                         Human / Controller
                                  |
                                  v
+------------------------------------------------------------+
|                           MOBIUS                           |
|                                                            |
|  Governance   Runtime   Evidence   Repository   Knowledge   |
+---------------+----------+----------+------------+----------+
                |          |          |            |
                |          |          |            +--> Obsidian
                |          |          +--> Git / Worktree / CI / PR
                |          +--> tests / diff / validation / audit
                +--> Codex / Hermes / future runtimes
```

## Controller-first 工程治理

Möbius 最重要的原则之一是：**Agent 写完代码，不等于工程阶段已经完成。**

```text
PLANNED -> ADMITTED -> IMPLEMENTING -> SUBMITTED -> REVIEWING
                                      ^              |
                                      +---- FIX -----+
                                                     +--> BLOCK
                                                     +--> PASS
                                                           |
                                                           v
                                                  MERGE_AUTHORIZED
                                                           |
                                                           v
                                                        MERGED
                                                           |
                                                           v
                                                        CLOSED
```

机械执行可以高度自动化，但架构判断、风险接受、安全敏感决策、Stage Admission 和 Merge Authority 必须保持显式治理。

## Agent Runtime

```text
AgentRuntime
├── CodexRuntime      # 第一参考实现
├── HermesRuntime     # 计划中的第二 Runtime
└── FutureRuntime     # 通过明确准入后加入
```

统一 Runtime 边界计划覆盖 Agent 发现、上下文读取、持久化重新接入、Bounded Task 派发、状态观察、中断与结果收集等能力。

Codex 是第一条真实产品验证路径。Hermes 应当扩展已经验证过的控制平面，而不是重新定义 Möbius。

## Evidence-first：先证明，再判断

Möbius 不会因为某个 Agent 回答 `done` 就认为任务已经完成。Evidence Plane 将尽可能自动收集 changed files、Git diff、tests、coverage、lint/type checks、build、migration、Docker/service health、runtime errors、CI、PR 状态和 contract deviations 等机器可验证事实。

> **Automate evidence, not judgment. / 自动化证据，不自动化判断。**

这样既减少重复汇报和上下文浪费，也保留 Controller 的独立审查能力。

## Repository Control / Git Orchestrator

Git 在 Möbius 中是一等子系统，而不是让 Agent 自由执行的一堆 shell 命令。

目标 Repository Plane 包括仓库检查、branch 创建/复用、worktree 生命周期、Role 与 workspace 绑定、commit/push、PR 创建/更新、CI 观察、Merge Authorization、自动 merge 与 merge 后 main/worktree 同步。

Merge Authorization 将绑定到 Controller 实际审查过的 **PR head SHA**。只要代码发生变化，旧授权立即失效。

> **Automate Git mechanics. Preserve Git authority. / 自动化 Git 操作，但保留 Git 权限治理。**

## Knowledge Memory + Obsidian

Möbius 不只管理一次执行，还要保存整个 AI 工程组织真正学到的东西，包括架构决策、Stage 记录、Controller 决策、失败与修复、Runtime 兼容性发现、工程经验、研究主线、产品假设和 Value Threads。

Möbius 的机器可读结构化状态仍然是工程 Source of Truth；Obsidian 则承担第一等的 **Human Knowledge Interface**：

```text
Möbius structured knowledge
          |
          v
Knowledge Projection Engine
          |
          v
Obsidian-compatible Markdown
          |
          v
阅读 / 双链 / 批注 / 研究 / 长期积累
```

初始方向保持单向：`Möbius -> Obsidian`。未来若引入双向同步，必须另外定义 provenance、permission 和 conflict resolution。

## Bounded Engineering Contract

Möbius 不给 Worker 一个无限制的模糊目标，而是下发明确 Task Packet，其中可以包含 Project、Version/Stage、Role、Runtime、Objective、Frozen Scope、Non-goals、Allowed Files、Permission Boundary、Acceptance Criteria、Required Validation、Evidence Requirements、Failure Rules 和 Report Format。

为了避免普通 bug 反复污染总架构，故障被分为：

| 类型 | 含义 | 默认处理 |
|---|---|---|
| F1 | 实现缺陷 | 当前 Stage 内直接修复 |
| F2 | Runtime 兼容性问题 | 修 Runtime Adapter |
| F3 | Contract 设计问题 | Controller 修改 Contract / ADR |
| F4 | 架构前提被推翻 | 停止流水线并显式重新设计 |

## 最终体验

```text
你：
继续 FlowTracer。

Möbius：
当前阶段：BE-7。
Backend Role 已解析为 CodexRuntime。
冻结技术契约已加载。
Worktree 已准备。
任务已派发。
实现完成。
82 tests passed。
CI passed。
独立审查发现 1 个 P2。
修复任务已自动返回 Backend。
第二轮验证通过。
等待最终 Merge Authorization。

合并后：
Stage Record 已归档。
Engineering Knowledge 已提取。
Obsidian Project Memory 已更新。
下一阶段等待准入。
```

最终目标是让人只需要思考 **项目、架构、阶段、风险和决策**，而不是不断切换 Agent 对话、复制粘贴、手动操作 Git 和整理知识。

## v0.1 → v1.1 路线

| 版本 | 目标 |
|---|---|
| **v0.1** | Codex 持久化 Thread 发现基础 |
| **v0.2** | 结构化 Thread / Context 读取 |
| **v0.3** | Resume / Persistent Attachment |
| **v0.4** | Bounded Task Dispatch |
| **v0.5** | 统一执行状态模型 |
| **v0.6** | Evidence / Validation Manifest |
| **v0.7** | Role Registry + Project Binding |
| **v0.8** | 可执行 Stage Gate 方法论 |
| **v0.9** | 最小 MCP Control Surface |
| **v1.0** | 完整 Codex-first Engineering Control Plane |
| **v1.1** | Repository Control + 工作流自动化 + Knowledge Projection + Hermes / Multi-runtime 扩展路径 |

Repository Automation、Obsidian 与 Hermes 都建立在已经验证的控制平面之上，不允许绕过最先需要证明的 Codex Runtime 闭环。

## 技术文档

- [`docs/00-PROJECT-CONTROL.md`](docs/00-PROJECT-CONTROL.md) — 顶层治理基线
- [`docs/02-R0-INTEGRATION-DECISION.md`](docs/02-R0-INTEGRATION-DECISION.md) — Codex 集成决策
- [`docs/10-MASTER-TECHNICAL-DESIGN.md`](docs/10-MASTER-TECHNICAL-DESIGN.md) — CodexRuntime 实现基线
- [`docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md`](docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md) — 版本化施工路线
- [`docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md`](docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md) — Repository Control 架构
- [`docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md`](docs/14-AI-ENGINEERING-OS-ARCHITECTURE.md) — Multi-runtime 架构
- [`docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md`](docs/15-MOBIUS-KNOWLEDGE-ARCHITECTURE.md) — Knowledge + Obsidian 架构
- [`docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md`](docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md) — **整个产品的权威目标架构**
- [`docs/21-MOBIUS-CROSS-PLANE-CONTRACT.md`](docs/21-MOBIUS-CROSS-PLANE-CONTRACT.md) — 五大平面之间的契约与权限边界

## 当前状态

**Pre-alpha / Architecture-first implementation。**

当前施工顺序刻意保持狭窄：

```text
Codex foundation
-> 发现真实 persistent threads
-> 在真实本地 Codex 环境验证
-> Controller Gate
-> read / resume / dispatch / status
```

我们现在先把完整架构写清楚，是为了让后续实现沿稳定施工图逐层填充，而不是每开发一个版本就重新设计一次产品。

正式产品名：**Möbius / 莫比乌斯**。  
历史代号：**Codex Domination**。

## License

Möbius 使用 [MIT License](LICENSE)。

---

如果你认同这种 AI 软件工程组织方式，测试早期 Runtime 闭环、提交 Issue、贡献 Runtime Adapter，或者为仓库点一个 Star，都会帮助 Möbius 继续成熟。
