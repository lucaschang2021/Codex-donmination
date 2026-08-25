# Codex Domination — Project Control / 项目控制基线

## 1. Mission / 使命

Codex Domination exists to provide a narrow control bridge for multiple persistent Codex threads.

Codex Domination 的目标，是为多个持久化 Codex 对话提供一个狭窄、结构化、可审计的控制桥。

The project is not a general autonomous software factory. Its first responsibility is to remove manual relay work between a controller and specialist Codex roles while preserving explicit human/controller authority.

本项目不是通用“自主软件工厂”。第一责任是减少总控与不同 Codex 专业角色之间的人工中转，同时保留明确的人类/总控最终控制权。

## 2. v0.1 Frozen Objective / v0.1 冻结目标

Prove one reliable end-to-end loop:

验证一条可靠的端到端控制闭环：

```text
Controller
  → discover persistent Codex threads
  → read one selected thread
  → dispatch one bounded task
  → observe execution state
  → receive a deterministic completion/failure signal
```

The following capabilities define v0.1:

- `list_threads`
- `read_thread(thread_id)`
- `send_task(thread_id, prompt)`
- `watch_status(thread_id)` or equivalent
- minimal MCP-compatible external control surface

以下能力构成 v0.1：

- 列出持久化 Codex 对话
- 读取指定对话
- 向指定对话派发有边界的任务
- 观察状态并获得确定性结束信号
- 提供最小 MCP 兼容外部控制面

## 3. Non-goals / 明确不做

v0.1 MUST NOT expand into:

- graphical dashboard
- Obsidian / knowledge-base integration
- automatic PR creation or merging
- autonomous release authority
- generic multi-model orchestration
- broad project-management features
- UI scraping as the default transport

v0.1 不得扩张到：

- 图形化控制台
- Obsidian / 知识库
- 自动 PR 创建或合并
- 自主发布权限
- 通用多模型编排
- 大型项目管理功能
- 以 UI 抓取作为默认传输方案

## 4. Governance / 治理

The project follows a controller-first stage-gate model.

本项目采用总控优先的 Stage Gate 模式。

```text
Research freeze
    ↓
Implementation task admitted
    ↓
Developer executes
    ↓
Mechanical evidence collected
    ↓
Controller independently reviews
    ↓
PASS / FIX / BLOCK
    ↓
Merge / next stage
```

Rules:

1. No implementation assumption is treated as stable until the integration surface has been validated.
2. Each stage has explicit scope, non-goals and acceptance criteria.
3. Mechanical evidence may be automated; architectural/security judgment may not be silently automated away.
4. A developer role may report completion, but only the controller admits the next stage.
5. New product ideas go to Roadmap/Future, not into the current stage by default.

规则：

1. 在完成集成面验证前，不把任何实现假设视为稳定事实。
2. 每个阶段必须有明确范围、禁止项和验收标准。
3. 机械证据可以自动化，但架构/安全判断不得被静默取消。
4. 开发角色可以报告完成，但只有总控可以准入下一阶段。
5. 新想法默认进入 Roadmap/Future，不直接污染当前阶段。

## 5. Stage Plan / 阶段计划

### R0 — Integration Research / 集成面研究

Goal: determine the supported way to discover, read, address and control persistent Codex threads.

Deliverable:
- short technical decision note
- confirmed transport/protocol
- confirmed thread identity model
- confirmed read/write/status primitives
- explicit rejected assumptions

Exit gate: Controller confirms there is at least one technically defensible path to implement the v0.1 loop.

### BE-1 — Read Bridge / 读取桥

Goal: implement `list_threads` and `read_thread` against the frozen integration path.

Exit gate:
- at least two persistent threads can be discovered
- a chosen thread can be read without manual copy/paste
- missing/unavailable threads return deterministic errors
- no UI scraping unless R0 explicitly authorizes it

### BE-2 — Dispatch & Status / 派发与状态

Goal: implement bounded task dispatch and terminal status observation.

Exit gate:
- controller can target one existing thread
- task submission is explicit
- completion/failure/timeout semantics are defined
- no hidden merge/release authority

### INT-1 — MCP Surface / MCP 控制面

Goal: expose the minimum structured external interface.

Exit gate:
- discovery → read → dispatch → status works through the external interface
- schemas are narrow and documented
- one reproducible end-to-end demo exists

### REL-0 — v0.1 Pre-release / v0.1 预发布

Goal: package a reproducible pre-alpha release with documentation and known limitations.

Exit gate:
- install/run instructions
- architecture note
- threat/permission boundary note
- tests for critical paths
- no known P1 issue

## 6. Risk Priorities / 风险优先级

Highest-risk areas for controller review:

- authentication and local process permissions
- arbitrary task dispatch
- thread mis-targeting
- stale or ambiguous execution status
- unsafe command/tool escalation through delegated agents
- hidden assumptions about Codex persistence or APIs
- accidental autonomous GitHub/release actions

总控重点审查：认证与本地进程权限、任意任务派发、thread 误投递、状态歧义、工具权限升级、对 Codex 持久化/API 的未经验证假设，以及意外获得自主合并/发布能力。

## 7. Definition of Success / 成功定义

v0.1 is successful when a controller can operate multiple persistent Codex roles without manually switching windows for the basic control loop, while retaining explicit final authority.

当总控能够在不手工切换窗口的情况下完成“发现 → 读取 → 派发 → 状态观察”的基础闭环，并仍保留最终决策权时，v0.1 即视为成功。

## 8. Long-range Repository Control Governance / 长期仓库控制治理

The frozen v0.1 scope above remains unchanged. However, the approved long-range architecture now includes a first-class **Repository Control Plane / Git Orchestrator**.

长期演化中，Codex Domination 将自动化正常开发所需的分支、worktree、commit、push、PR、CI、修复回流、merge 与同步等机械操作，但不取消总控的最终授权。

Governance rules:

1. Agent task completion is never merge authorization.
2. Green tests/CI are evidence, not merge authorization.
3. `PASS`, `MERGE_AUTHORIZED`, and `MERGED` are separate states.
4. Merge authorization must bind to a concrete PR and exact head SHA.
5. Any new commit invalidates prior merge authorization.
6. Worker roles cannot self-authorize merge/release.
7. Destructive Git/repository operations require higher authority than ordinary development operations.
8. Repository automation is introduced only in the version stages defined by the versioned roadmap; it must not leak into the frozen v0.1 scope.

Authoritative architecture references:

- `docs/11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md`
- `docs/12-GIT-ORCHESTRATOR-ARCHITECTURE.md`
- `docs/13-ARCHITECTURE-AMENDMENT-REPOSITORY-CONTROL.md`
