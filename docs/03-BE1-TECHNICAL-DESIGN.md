# BE-1 Technical Design / 技术设计

Status: Draft implementation completed; awaiting real local Codex verification.

状态：实现草案已完成，等待真实本地 Codex 环境验收。

## 1. Objective / 目标

BE-1 provides the first executable slice of Codex Domination: discover persistent Codex threads through the official OpenAI Codex Python SDK and present them through a deterministic read-only CLI.

BE-1 提供 Codex Domination 的第一段可执行能力：通过 OpenAI 官方 Codex Python SDK 发现持久化 Codex thread，并通过确定性的只读 CLI 输出结果。

The stage intentionally excludes thread mutation, task dispatch, status streaming, MCP, UI and GitHub orchestration.

本阶段刻意排除 thread 修改、任务派发、状态流、MCP、UI 和 GitHub 自动化。

## 2. Upstream dependency / 上游依赖

Primary dependency:

```text
openai-codex
```

The official SDK launches the local Codex App Server internally and exposes a public `thread_list(...)` method. BE-1 therefore does not implement a private JSON-RPC transport.

官方 SDK 会在内部启动本地 Codex App Server，并公开 `thread_list(...)`。因此 BE-1 不自行实现私有 JSON-RPC 传输层。

Conceptual flow:

```text
codex-domination CLI
        |
        v
ThreadDiscoveryService
        |
        v
openai-codex Python SDK
        |
        v
codex app-server --listen stdio://
        |
        v
persistent Codex thread store
```

## 3. Module boundary / 模块边界

### `src/codex_domination/discovery.py`

Responsibilities:

- open an official Codex SDK client lifecycle;
- call `thread_list(limit=...)`;
- convert generated SDK response models into a small internal stable model;
- reject malformed upstream data early;
- perform no write/control action.

职责：

- 管理官方 Codex SDK 客户端生命周期；
- 调用 `thread_list(limit=...)`；
- 将 SDK 生成模型转换为项目内部稳定小模型；
- 对异常上游数据尽早失败；
- 不执行任何写入或控制行为。

### `ThreadSummary`

Current normalized contract:

```text
thread_id: str
name: str | None
cwd: str | None
preview: str | None
updated_at: int | str | None
```

This model deliberately contains fewer fields than the upstream SDK. Codex Domination owns this internal contract so future upstream changes do not automatically leak into higher layers.

该模型刻意少于上游 SDK 字段。Codex Domination 自己拥有这一内部契约，以避免上游字段变化直接污染更高层。

### `src/codex_domination/cli.py`

Current public command:

```bash
codex-domination threads
codex-domination threads --json
codex-domination threads --limit 25
```

CLI guarantees:

- `--limit` must be a positive integer when supplied;
- empty thread lists are a successful result;
- SDK/App Server failures return a concise error and non-zero exit code;
- JSON output is deterministic and UTF-8 safe;
- BE-1 never resumes or mutates a thread.

## 4. Data flow / 数据流

```text
User command
   |
   v
argparse validation
   |
   v
ThreadDiscoveryService.list_threads()
   |
   v
Codex() context manager
   |
   v
Codex.thread_list(limit=...)
   |
   v
SDK ThreadListResponse
   |
   v
normalize_thread_list_response()
   |
   v
list[ThreadSummary]
   |
   +--> text renderer
   |
   +--> JSON renderer
```

No persistence is introduced in BE-1. Every invocation performs a fresh read through the SDK.

BE-1 不引入自己的持久化层；每次调用都通过 SDK 做一次新的读取。

## 5. Error contract / 错误契约

### Input errors

Invalid CLI input such as `--limit 0` or `--limit -1` is rejected before SDK startup.

### Upstream runtime errors

Examples include:

- Codex runtime cannot be found;
- App Server fails to launch;
- initialization fails;
- thread listing fails.

These are converted at the CLI boundary to:

```text
codex-domination: failed to discover Codex threads: <reason>
```

with a non-zero exit code.

### Upstream schema errors

Normalization rejects:

- non-list `data` payloads;
- thread entries with missing/blank IDs;
- non-mapping response objects that cannot be converted through `model_dump(...)`.

## 6. Testing strategy / 测试策略

BE-1 currently uses two validation layers.

### Unit/contract tests

Tests cover:

- normal thread normalization;
- empty list behavior;
- missing thread ID rejection;
- service invocation of the official `thread_list` surface;
- positive `--limit` validation.

### CI

GitHub Actions currently runs:

```text
Install
Ruff
Pytest
```

on Python 3.12.

CI proves package installation and deterministic unit behavior, but it does not prove access to a real user's persistent Codex threads.

## 7. Real-environment acceptance / 真实环境验收

BE-1 cannot pass the final Controller Gate until this command succeeds on a real workstation with Codex installed and configured:

```bash
codex-domination threads --json
```

Required evidence:

1. process exits successfully;
2. at least one real persistent Codex thread is returned when such threads exist;
3. IDs are non-empty and stable enough to be reused by later stages;
4. `cwd`, `name`, `preview` and timestamp behavior are inspected against actual SDK output;
5. no thread is resumed or mutated merely by listing;
6. startup failure behavior is understandable when Codex is unavailable.

The final merge decision remains blocked until this local verification is recorded.

最终 merge 决策在这一步完成之前保持阻塞。

## 8. Security and permission boundary / 安全与权限边界

BE-1 is intentionally read-only.

It does not:

- bypass Codex authentication;
- alter approval policy;
- alter sandbox policy;
- resume a thread;
- start a turn;
- send instructions;
- approve tool execution;
- merge code.

The bridge must inherit Codex's own authentication and runtime boundaries rather than attempting to bypass them.

## 9. Known risks / 已知风险

### Upstream SDK churn

The official Python SDK is still evolving. Generated model shapes may change. The normalization layer is the primary compatibility buffer.

### Runtime/SDK version coupling

The SDK may depend on a pinned Codex runtime package. Installation and real-runtime compatibility must be validated whenever the SDK version changes.

### Thread visibility semantics

`thread_list` filtering, archived behavior, source kinds and persistence semantics must be verified against real user data before BE-2 assumes all desired desktop conversations are visible.

### Metadata assumptions

Fields such as `name`, `preview`, `cwd` and timestamps may be missing or differ across thread sources. Higher layers must treat them as optional until proven otherwise.

## 10. Stage gate / 阶段准入

BE-1 may merge only when all conditions are true:

- [x] implementation uses the official SDK;
- [x] no private JSON-RPC transport exists;
- [x] unit tests pass;
- [x] Ruff passes;
- [x] CI passes on the initial implementation;
- [x] Controller code review completed and one input-boundary defect was fixed;
- [ ] post-fix CI passes;
- [ ] real Windows/local Codex discovery succeeds;
- [ ] actual returned metadata is inspected;
- [ ] Controller records final PASS.

## 11. BE-2 boundary / 下一阶段边界

BE-2 should not begin merely because BE-1 code exists. After BE-1 passes, the next narrow stage should add **read-only selected-thread inspection** using the official thread read surface.

BE-2 should still exclude task dispatch and autonomous control.

BE-2 不应因为 BE-1 已经有代码就自动开始。只有 BE-1 正式通过后，下一阶段才加入“读取指定 thread”的只读能力，并继续排除任务派发和自主控制。
