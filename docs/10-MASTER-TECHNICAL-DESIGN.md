# Möbius — Codex Runtime Technical Baseline / Codex 运行时技术基线

> Status: **Implementation Baseline / 实现基线**
>
> Canonical target architecture: [`20-MOBIUS-MASTER-ARCHITECTURE-v1.md`](./20-MOBIUS-MASTER-ARCHITECTURE-v1.md)
>
> Historical codename: `Codex Domination`.

This document defines the **Codex-first implementation baseline** inside the wider Möbius architecture. It no longer defines the whole product. The whole product is the five-plane Möbius system: Governance, Runtime, Evidence, Repository and Knowledge.

Möbius remains Codex-first during implementation, but not Codex-only. Codex is the reference runtime; Hermes is the first planned additional runtime.

---

## 1. Purpose / 目的

The first engineering proof is intentionally narrow:

```text
Controller
  → discover persistent Codex threads
  → read structured context
  → resume/attach
  → dispatch one bounded task
  → observe deterministic execution state
  → collect a structured result
```

This foundation must work reliably before Möbius admits higher-level automation such as Stage Gate execution, Repository Control, Obsidian Knowledge Projection or Hermes integration.

---

## 2. Runtime Architecture / 运行时架构

```text
Möbius Governance
      │
      ▼
AgentRuntime Interface
      │
      ▼
CodexRuntime
      │
      ▼
Official Codex SDK / App Server
      │
      ▼
Persistent Codex Threads / Turns
```

All Codex-specific behavior stays behind `CodexRuntime`. Upper layers must consume normalized Möbius models rather than SDK-specific response objects.

Candidate normalized runtime surface:

```text
discover()
read_context(agent_id)
attach(agent_id)
dispatch(agent_id, task_contract)
watch(execution_id)
interrupt(execution_id)
collect_result(execution_id)
```

Unsupported semantics fail explicitly. Möbius must never fake parity between runtimes.

---

## 3. Codex Integration Baseline / Codex 集成基线

Preferred integration path:

**official OpenAI Codex Python SDK + local Codex App Server**.

Required semantic distinctions:

- discovery answers which persistent threads exist;
- read returns persisted context/history;
- attach/resume re-enters a persistent thread;
- dispatch starts new bounded work;
- status/watch observes live execution;
- result returns terminal output;
- approval/sandbox behavior remains visible and is not bypassed.

UI scraping is not the primary transport.

---

## 4. Core Runtime Models / 核心模型

```text
AgentIdentity
- runtime
- agent_id
- display_name?
- workspace?
- updated_at?

ContextSnapshot
- agent_id
- items/events
- cursor?
- truncated

Execution
- execution_id
- agent_id
- task_id
- upstream_turn_id?
- state
- created_at
- updated_at

ExecutionState
- UNKNOWN
- ACCEPTED
- RUNNING
- WAITING_APPROVAL
- BLOCKED
- COMPLETED
- FAILED
- INTERRUPTED
- TIMED_OUT

RuntimeResult
- execution_id
- terminal_state
- final_output?
- artifacts?
- errors?
```

Thread IDs and turn IDs remain upstream identities. Möbius task/stage IDs remain orchestration identities.

---

## 5. Runtime Modules / 运行时模块

### Runtime Adapter
Owns SDK/App Server initialization, shutdown, version compatibility and exception normalization.

### Discovery Service
Discovers persistent Codex threads and produces deterministic normalized identities.

### Context Reader
Reads one exact thread without mutation and normalizes persisted history.

### Attachment Manager
Resumes/re-attaches to a persistent thread only when live interaction is required.

### Task Dispatcher
Submits exactly one bounded task to exactly one known target and returns a deterministic receipt.

### Status / Event Watcher
Normalizes live upstream events into the small Möbius lifecycle model.

### Result Collector
Correlates the terminal execution result with the Möbius task identity and preserves runtime-native diagnostics when useful.

---

## 6. Boundary With Governance / 与治理层边界

The Codex runtime may execute work. It does not own engineering authority.

It must not decide:

- stage admission;
- architecture changes;
- PASS / FIX / BLOCK;
- merge authorization;
- release authorization;
- knowledge truth policy.

Those decisions belong to the Möbius Governance Plane and Controller.

---

## 7. Boundary With Repository Control / 与仓库控制边界

Codex may modify files inside its declared workspace if its task permits it. Repository lifecycle is owned by the Repository Plane.

Therefore:

```text
Task completion ≠ commit authorization
Task completion ≠ PR approval
Task completion ≠ merge authorization
```

Repository Control owns branch/worktree validation, commit/push/PR mechanics, CI correlation, exact-state merge authorization and post-merge synchronization.

---

## 8. Boundary With Evidence / 与证据层边界

A worker response such as “done” is a claim, not proof.

The Evidence Plane independently collects mechanical facts such as:

- changed files and diff metadata;
- tests / coverage;
- lint / type checks;
- build / migration results;
- Docker/service health;
- runtime failures;
- CI / PR state;
- contract deviations.

Core invariant:

> **Automate evidence, not judgment.**

---

## 9. Boundary With Knowledge / 与知识层边界

Codex conversation history is not the long-term engineering knowledge system.

Useful outcomes are transformed into structured Möbius knowledge records, then optionally projected to Obsidian.

```text
Codex execution
   ↓
Evidence + Controller decision
   ↓
Structured Möbius knowledge
   ↓
Obsidian projection
```

Obsidian remains the human knowledge interface, not the runtime source of truth.

---

## 10. Error Model / 错误模型

Canonical runtime errors should include:

```text
RUNTIME_UNAVAILABLE
RUNTIME_INCOMPATIBLE
AUTH_REQUIRED
AGENT_NOT_FOUND
AGENT_AMBIGUOUS
AGENT_UNAVAILABLE
INVALID_ARGUMENT
DISPATCH_REJECTED
APPROVAL_REQUIRED
EXECUTION_FAILED
EXECUTION_INTERRUPTED
EXECUTION_TIMEOUT
TRANSPORT_CLOSED
UPSTREAM_PROTOCOL_ERROR
INTERNAL_ERROR
```

No blanket retry is allowed for non-idempotent dispatch.

---

## 11. Security Invariants / 安全不变量

1. Do not bypass Codex authentication, sandboxing or approval policy.
2. Every control-critical action targets an exact identity.
3. Read-only capabilities stay separable from write/dispatch capabilities.
4. Secrets must not be copied into logs, evidence manifests or knowledge projections.
5. Runtime capability does not imply repository or stage authority.
6. Unknown upstream states fail conservatively.
7. Real-runtime validation is required before stage completion where the contract depends on runtime behavior.

---

## 12. Testing Strategy / 测试策略

### Unit
- normalization;
- argument validation;
- state mapping;
- deterministic rendering;
- error mapping.

### Contract
- adapter calls supported SDK/App Server primitives;
- no runtime-specific models leak above the adapter boundary;
- unsupported capabilities fail explicitly.

### Real runtime
- discover real persistent threads;
- read a known thread;
- resume a known thread;
- dispatch a bounded harmless task;
- observe a terminal state;
- verify deterministic cleanup/error behavior.

CI is evidence. Controller review is the gate.

---

## 13. Codex-First Delivery Sequence / Codex 优先交付顺序

```text
v0.1  discovery
v0.2  structured read
v0.3  resume / attachment
v0.4  bounded dispatch
v0.5  normalized status
v0.6  evidence
v0.7  role + project binding
v0.8  Stage Gate
v0.9  MCP control surface
v1.0  complete Codex-first control plane
v1.1  Repository Control + Knowledge Projection + Hermes path
```

Each version requires implementation, tests, real-environment validation when applicable, Controller independent review and documented PASS.

---

## 14. Current Freeze / 当前冻结结论

- Official Codex SDK/App Server is the selected first runtime integration.
- Python remains the v0.x bridge implementation language.
- CodexRuntime is a reference implementation of the wider AgentRuntime concept.
- Controller-first governance is mandatory.
- v0.1 remains narrow: prove discovery before expanding authority.
- Hermes, Git automation and Obsidian projection are target-architecture capabilities and must not bypass the Codex foundation gates.
- The canonical whole-product architecture is `20-MOBIUS-MASTER-ARCHITECTURE-v1.md`.

**Next engineering action:** finish real Codex discovery validation, pass the Controller gate, then admit structured read.
