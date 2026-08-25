# R0 Integration Decision / R0 集成决策

Status: **ACCEPTED for v0.1**  
状态：**v0.1 已接受**

## Decision / 决策

Codex Domination v0.1 will target the **official Codex App Server execution layer** as the primary integration path.

Codex Domination v0.1 将以 **官方 Codex App Server 执行层**作为首选集成路径。

The project will not use UI scraping as its primary architecture. UI automation remains a fallback only if a required capability is absent from supported App Server behavior.

项目不会把 UI 抓取作为核心架构。只有当某个必要能力无法通过受支持的 App Server 行为获得时，才考虑把 UI 自动化作为后备方案。

## Why this gate can pass / 为什么 R0 可以通过

Current upstream Codex sources expose the exact primitive family required by the v0.1 control loop:

当前上游 Codex 已暴露 v0.1 控制闭环所需的关键原语族：

1. **Thread discovery** — `thread/list` exists, with structured filtering/sorting and persistent thread metadata.
2. **Thread history/state inspection** — App Server exposes read/resume primitives and structured thread/turn data.
3. **Persistent thread resume/rejoin** — `thread/resume` explicitly supports resuming a stored thread by `thread_id`; if the thread is already running, App Server rejoins it.
4. **Live event subscription semantics** — resuming a running thread sends history/state and subscribes the client for subsequent updates.
5. **Task dispatch path** — the App Server client/test surfaces support sending messages into Codex sessions/threads and continuing the same turn when user input is requested.
6. **External transports exist** — App Server semantics are available across process boundaries through JSON-RPC over stdio/websocket, while upstream also maintains an in-process typed client.

1. **Thread 发现** —— 存在 `thread/list`，可结构化返回并筛选持久化 thread 元数据。
2. **Thread 历史/状态读取** —— App Server 提供 read/resume 等结构化 thread/turn 能力。
3. **持久化恢复/重连** —— `thread/resume` 明确支持按 `thread_id` 从磁盘恢复；若 thread 正在运行，则重新加入该运行中的 thread。
4. **实时事件订阅语义** —— 对运行中 thread 执行 resume 时，App Server 会返回历史/状态并订阅后续更新。
5. **任务派发路径** —— 官方 App Server 客户端/测试客户端支持向 Codex session/thread 发送消息，并可在需要用户输入时继续同一 turn。
6. **存在外部传输层** —— App Server 可通过 stdio/websocket 的 JSON-RPC 跨进程使用，上游同时维护进程内 typed client。

## Important semantic distinction / 关键语义区分

`thread/read` and `thread/resume` must not be treated as equivalent.

不得把 `thread/read` 与 `thread/resume` 当成等价操作。

- `thread/read` is suitable for state/history inspection.
- `thread/resume` is the operation that re-enters an existing thread and is the basis for receiving subsequent live updates.

- `thread/read` 适合读取状态与历史。
- `thread/resume` 才是重新加入既有 thread、并继续接收后续实时更新的关键操作。

This distinction is now a frozen v0.1 architecture rule.

这一点现在被冻结为 v0.1 架构规则。

## Thread identity assumption / Thread 身份假设

For v0.1, `thread_id` is treated as the canonical controller-visible identifier whenever upstream provides it. Upstream protocol comments explicitly recommend preferring `thread_id` for resume when possible.

v0.1 中，只要上游提供 `thread_id`，总控就将其视为首选规范标识。上游协议注释也明确建议在可能时优先使用 `thread_id` 进行 resume。

However, Codex Domination must not yet promise that an ID is globally stable across every future Codex release or storage migration. Compatibility handling belongs in the adapter layer.

但 Codex Domination 暂不承诺该 ID 在未来所有 Codex 版本或存储迁移中永久稳定；兼容逻辑应封装在适配层。

## Permission and approval boundary / 权限与审批边界

A resumed thread can carry or override runtime configuration such as approval policy, sandbox mode, model/provider, cwd and related settings. Therefore Codex Domination must treat dispatch as a privileged operation and preserve explicit controller authority.

恢复 thread 时可携带或覆盖 approval policy、sandbox、model/provider、cwd 等运行时设置。因此 Codex Domination 必须把任务派发视为高权限操作，并保留显式总控权。

v0.1 rules:

- never silently broaden sandbox permissions;
- never silently weaken approval policy;
- never auto-merge or auto-release;
- always target an explicit `thread_id` for writes;
- surface approval-blocked, failed, interrupted and completed states distinctly when upstream events permit.

v0.1 规则：

- 不得静默扩大 sandbox 权限；
- 不得静默弱化 approval policy；
- 不得自动合并或自动发布；
- 写操作必须显式指定 `thread_id`；
- 在上游事件允许时，明确区分等待审批、失败、中断、完成等状态。

## Architecture implications / 架构影响

The v0.1 bridge should be split into:

```text
AppServerTransport
    ↓
ThreadRegistry      -> thread/list
ThreadReader        -> thread/read (+ paginated turns/items if needed)
ThreadSession       -> thread/resume for live attachment
TaskDispatcher      -> send bounded user/task input
StatusWatcher       -> normalize live thread/turn/item notifications
EventNormalizer     -> stable internal event model
MCPControlSurface   -> minimal controller-facing tools
```

v0.1 does **not** need its own autonomous scheduler, GUI dashboard, GitHub merger or knowledge base.

v0.1 **不需要**自建自主调度器、大型 GUI、GitHub 自动合并器或知识库。

## Rejected assumptions / 被否决的假设

- Rejected: UI scraping is required to read Codex conversations.
- Rejected: a custom unofficial database reader should be the primary path.
- Rejected: `thread/read` alone is enough for live monitoring.
- Rejected: the controller can safely infer the target thread from free text.
- Rejected: v0.1 should clone the full Codex UI/DevOS experience.

- 否决：读取 Codex 对话必须依赖 UI 抓取。
- 否决：应把读取 Codex 私有存储/数据库作为首选方案。
- 否决：仅靠 `thread/read` 就足以做实时监控。
- 否决：总控可以仅靠自然语言自动猜目标 thread。
- 否决：v0.1 应复制完整 Codex UI/DevOS。

## Remaining implementation unknowns / 尚待实现验证的问题

R0 passes, but BE-1 must experimentally verify:

- exact initialization handshake for the chosen transport;
- exact request names/schemas used by the installed Codex version;
- pagination behavior for long thread history;
- event names that map to started/completed/failed/interrupted/approval-blocked states;
- behavior when a second client resumes a running thread;
- behavior when dispatch arrives while a turn is already active;
- cross-platform process startup details, especially Windows.

R0 已通过，但 BE-1 必须通过可复现实验确认：

- 所选 transport 的精确初始化握手；
- 当前安装 Codex 版本的精确请求名/schema；
- 长历史分页行为；
- started/completed/failed/interrupted/approval-blocked 对应事件；
- 第二个客户端加入运行中 thread 时的行为；
- turn 已运行时再次 dispatch 的行为；
- 跨平台启动细节，尤其 Windows。

## Gate result / 准入结论

**R0 PASS.** The project is no longer speculative at the architecture level. The next admitted stage is **BE-1: App Server connectivity + read-only thread discovery**.

**R0 通过。** 项目在架构层面不再是纯推测。下一准入阶段为 **BE-1：App Server 连接 + 只读 thread 发现**。
