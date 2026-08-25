# Codex Domination — v0.1 Architecture Draft / v0.1 架构草案

## Status / 状态

**Draft until R0 integration research is accepted.**

**在 R0 集成面研究通过前，本文件仅为草案。**

No protocol, SDK, process boundary or API described here is considered frozen until validated against the currently supported Codex integration surface.

在完成对当前 Codex 可用集成面的验证前，本文件中的协议、SDK、进程边界和 API 均不视为已冻结。

## 1. Target architecture / 目标架构

```text
┌──────────────────────────────┐
│      Controller / 总控       │
└──────────────┬───────────────┘
               │ structured tools
               ▼
┌──────────────────────────────┐
│     MCP / Control Surface    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│    Codex Domination Bridge   │
│                              │
│  Thread Registry             │
│  Thread Reader               │
│  Task Dispatcher             │
│  Status Watcher              │
│  Event Normalizer            │
└──────────────┬───────────────┘
               │ supported Codex integration
               ▼
┌──────────────────────────────┐
│  Persistent Codex Threads    │
│  Backend / Frontend / ...    │
└──────────────────────────────┘
```

## 2. Architectural boundaries / 架构边界

### Bridge owns / Bridge 负责

- discovering addressable persistent Codex threads
- normalizing thread metadata
- reading structured historical/current events
- dispatching explicitly targeted tasks
- observing execution state
- returning deterministic errors and terminal states
- exposing a small external control interface

### Bridge does not own / Bridge 不负责

- deciding product requirements
- autonomously approving code changes
- merging pull requests
- deciding releases
- replacing source control
- replacing the controller
- storing a general personal knowledge base

## 3. Internal components / 内部组件

### Thread Registry

Responsibilities:
- enumerate available threads
- resolve stable thread identifiers
- expose role/metadata mapping when available
- reject ambiguous targeting

### Thread Reader

Responsibilities:
- fetch useful thread history
- preserve event ordering
- distinguish user, agent, tool and system/execution events when available
- support bounded reads rather than unbounded transcript dumping

### Task Dispatcher

Responsibilities:
- target exactly one thread per explicit dispatch operation
- preserve caller-provided instruction content
- return submission acknowledgement or deterministic failure
- avoid hidden retries that could duplicate task execution

### Status Watcher

Responsibilities:
- observe active/running/terminal state
- distinguish success, failure, cancellation and timeout when the underlying surface supports them
- avoid inferring completion purely from natural-language agent text

### Event Normalizer

Responsibilities:
- map Codex-native events into a small bridge-owned schema
- preserve source event identifiers/timestamps where possible
- avoid fabricating unavailable fields

### MCP / External Control Surface

Candidate v0.1 tools:

```text
codex.list_threads()
codex.read_thread(thread_id, ...)
codex.send_task(thread_id, prompt)
codex.get_status(thread_id)
```

Names and schemas remain provisional until R0 is complete.

## 4. Candidate normalized models / 候选标准化模型

```yaml
ThreadSummary:
  id: string
  title: string | null
  role: string | null
  status: string | null
  updated_at: timestamp | null
```

```yaml
ThreadEvent:
  id: string | null
  thread_id: string
  kind: user_message | agent_message | tool | approval | diff | execution | unknown
  timestamp: timestamp | null
  payload: object
```

```yaml
DispatchReceipt:
  thread_id: string
  accepted: boolean
  dispatch_id: string | null
  error: object | null
```

```yaml
ExecutionStatus:
  thread_id: string
  state: idle | queued | running | succeeded | failed | cancelled | unknown
  terminal: boolean
  observed_at: timestamp
```

These are bridge-owned candidate models, not claims about the Codex-native schema.

以上只是 Bridge 自己的候选标准化模型，并不代表 Codex 原生 schema 必然如此。

## 5. Safety and permission boundary / 安全与权限边界

v0.1 must assume that sending text to an active coding agent can cause real local side effects through that agent's existing tool permissions.

v0.1 必须假设：向一个正在运行的编码 Agent 派发文本，可能通过该 Agent 已有工具权限造成真实本地副作用。

Therefore:

1. Every dispatch must identify a concrete target thread.
2. The bridge must not silently broaden permissions.
3. The bridge must not add autonomous merge/release authority.
4. Retries must not duplicate side-effecting tasks without explicit semantics.
5. Status must be distinguished from agent self-reported prose whenever possible.
6. Sensitive native events should not be exposed more broadly than necessary.

## 6. Persistence / 持久化

v0.1 should prefer minimal local state.

Potential bridge-owned state:
- thread aliases/role mappings
- last observed event cursor
- dispatch receipts
- normalized execution metadata

The Codex native thread history remains the authoritative conversation history whenever the supported integration exposes it.

如果受支持的 Codex 集成能够读取原生 thread history，那么 Codex 原生历史应继续作为权威对话记录；Bridge 不应无意义地复制整份对话数据库。

## 7. R0 questions that must be answered / R0 必答问题

Before implementation is frozen, research must answer:

1. What supported interface exposes persistent Codex threads today?
2. How are thread IDs represented and how stable are they?
3. Can existing thread history be read structurally?
4. Can a task be submitted to an existing thread?
5. What event/status subscription or polling mechanism exists?
6. Which operations require local process access, authentication or approval?
7. What happens when the Codex application restarts?
8. What are the compatibility/versioning expectations?
9. Which assumptions in this draft are false?

在这些问题回答清楚之前，不进入大规模实现。

## 8. v0.1 performance principle / v0.1 性能原则

The bridge exists partly to reduce duplicated natural-language relay. Therefore it should prefer bounded structured retrieval over repeatedly sending full transcripts to the controller.

Bridge 的一个核心价值就是减少自然语言中转开销，因此应优先进行有界、结构化读取，而不是每次把完整对话重新塞给总控。

A useful v0.1 metric is:

```text
manual relay steps avoided per completed controller → agent → controller loop
```

A future v0.2 metric can additionally measure context/token reduction.
