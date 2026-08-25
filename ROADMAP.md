# Codex Domination Roadmap / 路线图

This roadmap intentionally keeps the project narrow until the core control loop is proven.

这份路线图刻意限制项目范围，直到最核心的控制闭环被真正验证。

## Milestone 0 — Integration Research / 集成面验证

Goal: determine the safest supported way to interact with persistent Codex sessions.

目标：确认与持久化 Codex 会话交互的最稳妥、受支持方式。

Acceptance criteria / 验收标准:

- Identify supported Codex server/SDK/hook surfaces.
- Confirm thread discovery and thread identity semantics.
- Confirm whether historical messages and tool events are readable.
- Confirm whether tasks can be dispatched to an existing thread.
- Document authentication, local process and security boundaries.

- 明确 Codex Server / SDK / Hook 等可用集成面。
- 确认 thread 的发现方式和身份语义。
- 确认历史消息与工具事件是否可读取。
- 确认是否可以向既有 thread 派发任务。
- 记录认证、本地进程和安全边界。

## v0.1 — Control Bridge / 控制桥

Goal: one controller can interact with multiple persistent Codex threads through a minimal structured interface.

目标：一个总控能够通过最小结构化接口与多个持久化 Codex thread 交互。

Required capabilities / 必须能力:

- `list_threads`
- `read_thread`
- `send_task`
- `watch_status`
- minimal MCP-facing interface / 最小 MCP 接口
- explicit errors and timeouts / 明确错误与超时语义

Definition of done / 完成定义:

A real end-to-end demo proves:

真实端到端 Demo 必须证明：

```text
Controller
  → discovers Backend thread
  → reads recent context
  → sends a bounded task
  → watches execution state
  → receives completion state
```

## v0.2 — Evidence Layer / 证据层

Goal: reduce repeated natural-language reporting by extracting machine-readable execution evidence.

目标：通过自动提取机器可读证据，减少 Agent 反复写自然语言汇报的成本。

Planned capabilities / 计划能力:

- changed-file summary / 变更文件摘要
- diff metadata / diff 元数据
- test/validation result ingestion / 测试与验证结果收集
- task completion manifest / 任务完成清单
- token/context usage experiments / token 与上下文消耗实验
- event persistence / 事件持久化

Example manifest / 示例：

```yaml
role: backend
stage: BE-4
status: completed
changed_files: 11
tests:
  passed: 82
controller_review_required: true
```

## v0.3 — Controller Orchestration / 总控编排

Goal: encode a rigorous controller-first stage-gate workflow without removing human or controller judgment.

目标：把严格的“总控优先 + Stage Gate”流程编码进系统，但不移除人工与总控判断。

Planned capabilities / 计划能力:

- role registry / 角色注册
- stage admission / 阶段准入
- controller dispatch / 总控派发
- task rejection and rework / 驳回与返工
- retry and failure semantics / 重试与失败语义
- multi-project experiments / 多项目实验

## Later — Only if justified / 后续：只有必要时才做

These are intentionally outside the early roadmap:

以下内容刻意不进入早期路线图：

- graphical control center / 图形化控制中心
- GitHub orchestration / GitHub 自动编排
- knowledge-base or Obsidian integration / 知识库或 Obsidian 集成
- cross-model orchestration / 跨模型编排
- cloud-hosted team service / 云端团队服务
- autonomous release authority / 自主发布权限

They should be added only when real usage proves they reduce meaningful friction.

只有当真实使用证明这些能力能显著降低摩擦时，才应加入。

## Design rule / 设计铁律

> Automate evidence, transport and repetition. Preserve judgment, review and explicit authority.
>
> 自动化证据、传输与重复劳动；保留判断、复核与明确授权。
