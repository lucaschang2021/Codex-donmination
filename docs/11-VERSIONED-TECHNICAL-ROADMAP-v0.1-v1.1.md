# Möbius — Versioned Technical Roadmap v0.1 → v1.1

> Status: **Architecture-first delivery roadmap / 架构优先交付路线图**
>
> Canonical architecture: [`20-MOBIUS-MASTER-ARCHITECTURE-v1.md`](./20-MOBIUS-MASTER-ARCHITECTURE-v1.md)

Möbius is built in a deliberately staged way: the target system is designed first, then implementation fills that architecture one controlled version at a time.

The roadmap preserves one rule throughout:

> **Capability may expand; authority may not silently expand.**

---

## 1. Product Direction / 产品方向

**Möbius / 莫比乌斯 — Operating System for AI Engineering Teams.**

It is:

- Controller-first;
- Codex-first, not Codex-only;
- multi-runtime by architecture;
- evidence-driven;
- repository-aware;
- knowledge-preserving;
- Obsidian-compatible for human knowledge projection.

Five control planes:

```text
Governance
Runtime
Evidence
Repository
Knowledge
```

Core thesis:

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

---

## 2. Version-Gate Invariants / 版本门控不变量

Every version follows:

```text
architecture / contract
→ implementation
→ automated tests
→ real-environment validation where required
→ evidence package
→ Controller independent review
→ PASS / FIX / BLOCK
```

A version is not complete because code exists or CI is green.

Additional invariants:

1. exact agent/runtime identity for control-critical actions;
2. no hidden merge/release authority;
3. runtime-specific behavior stays behind adapters;
4. repository automation remains state-aware;
5. knowledge projection does not become a runtime dependency;
6. ordinary bugs are repaired locally;
7. F4 architectural invalidation requires an explicit ADR.

---

# 3. Version Plan / 版本计划

## v0.1 — Codex Discovery Foundation

**Outcome:** Möbius can connect to the supported local Codex runtime and discover persistent Codex threads without mutating them.

Adds:

- `CodexRuntime` bootstrap;
- Thread/Agent Registry baseline;
- normalized `AgentIdentity` / `ThreadSummary`;
- deterministic CLI and JSON output;
- initial runtime error model.

Non-goals:

- history read;
- resume;
- dispatch;
- live status;
- Git writes;
- Hermes;
- Obsidian;
- autonomous actions.

Exit gate:

```text
real local Codex
→ persistent threads discovered
→ stable IDs verified
→ empty state handled
→ startup/runtime errors deterministic
→ Controller PASS
```

---

## v0.2 — Structured Context Read

**Outcome:** Controller can inspect one exact persistent Codex context without UI copy/paste.

Adds:

- Context Reader;
- normalized history/event models;
- pagination/truncation rules;
- redaction boundary;
- deterministic missing-agent behavior.

Exit gate: one selected thread can be read reliably and rendered as structured context.

---

## v0.3 — Resume / Attachment

**Outcome:** Möbius can safely reattach to a persistent Codex context when live interaction is required.

Adds:

- Attachment Manager;
- availability classification;
- resume lifecycle;
- runtime restart handling;
- compatibility diagnostics.

Exit gate: persisted contexts can be rejoined deterministically and attachment state is observable.

---

## v0.4 — Bounded Task Dispatch

**Outcome:** Controller can submit one bounded task to one exact persistent agent identity.

Adds:

- Task Dispatcher;
- `TaskContract` baseline;
- dispatch IDs / receipts;
- duplicate-dispatch protection;
- explicit target validation.

Hard boundary:

```text
worker execution authority
≠ repository merge authority
≠ stage authority
```

Exit gate: one known agent receives one bounded task and returns a deterministic receipt.

---

## v0.5 — Execution Status

**Outcome:** Controller can observe a task through a normalized lifecycle.

Canonical states:

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

Adds:

- Status Watcher;
- Event Normalizer;
- timeout semantics;
- terminal result correlation;
- interrupt behavior where supported.

Exit gate:

```text
discover → read → attach → dispatch → status → result
```

works without manual Codex-window switching.

---

## v0.6 — Evidence Plane

**Outcome:** Möbius stops relying on worker self-report and begins collecting mechanical proof.

Adds:

- Evidence Collector;
- `ValidationManifest`;
- execution/evidence correlation;
- read-only repository evidence;
- validation command/result recording.

Candidate evidence:

```text
git status / diff
changed files
base/head SHA
tests / coverage
lint / type checks
build / migrations
Docker/service health
runtime errors
duration / retries
contract deviations
terminal result
```

Exit gate: every completed bounded task can produce a compact review packet.

---

## v0.7 — Project + Role Registry

**Outcome:** persistent agents become stable engineering roles inside explicit projects.

Adds:

- Project Registry;
- Role Registry;
- role ↔ runtime ↔ exact agent binding;
- project ↔ repository binding;
- role ↔ branch/worktree binding;
- per-role permission and validation profiles.

Example:

```text
Backend     → CodexRuntime → exact thread → backend worktree
Frontend    → CodexRuntime → exact thread → frontend worktree
Research    → future runtime binding
Integration → CodexRuntime → exact thread → integration worktree
```

Exit gate: role addressing remains convenient while exact identities remain auditable.

---

## v0.8 — Executable Stage Gate

**Outcome:** the Controller-first methodology becomes executable policy.

Adds:

- Stage Engine;
- admission rules;
- evidence requirements;
- PASS / FIX / BLOCK records;
- repository workspace admission;
- immutable decision history.

Canonical flow:

```text
PLANNED
→ ADMITTED
→ IMPLEMENTING
→ SUBMITTED
→ REVIEWING
→ FIX_REQUIRED / BLOCKED / PASS
→ MERGE_AUTHORIZED
→ MERGED
→ CLOSED
```

Exit gate: one real project stage is represented from admission through independent review.

---

## v0.9 — Structured Control Surface / MCP

**Outcome:** an external Controller such as ChatGPT can operate Möbius through narrow typed tools.

Tool families begin with:

```text
project.*
role.*
agent.*
task.*
evidence.*
stage.*
repo.read-only.*
```

No unrestricted shell is exposed as the default control surface.

Exit gate: the core workflow can run through the structured external interface.

---

## v1.0 — Codex-First Engineering Control Plane

**Outcome:** Möbius becomes a coherent pre-production AI engineering control plane around real persistent Codex roles.

Required capabilities:

- discovery;
- structured read;
- attach/resume;
- bounded dispatch;
- normalized status;
- evidence bundles;
- project/role bindings;
- Stage Gate;
- repository/worktree awareness;
- MCP/structured interface;
- audit records;
- reproducible end-to-end demo;
- documented security/permission boundaries.

Expected workflow:

```text
Controller selects project/stage
→ Möbius validates stage admission
→ resolves exact role/runtime/agent/workspace
→ loads frozen contract
→ dispatches bounded task
→ watches execution
→ collects evidence
→ Controller independently reviews
→ PASS / FIX / BLOCK
```

Explicitly excluded at v1.0:

- silent autonomous merge/release;
- broad multi-runtime claims without validation;
- Obsidian as runtime truth;
- dashboard-first product expansion.

---

## v1.1 — Closed-Loop AI Engineering OS

**Outcome:** repetitive engineering mechanics become automated around preserved Controller authority, and execution history becomes cumulative knowledge.

v1.1 integrates four major expansions.

### A. Repository Control / Git Orchestrator

May automate:

```text
inspect repository
prepare/reuse branch
prepare/reuse worktree
validate workspace
commit
push
open/update PR
watch CI
correlate review state
execute authorized merge
sync main/worktrees
```

Critical invariant:

```text
Controller PASS
+ MergeAuthorization(PR, exact_head_SHA)
+ repository state still matches
→ merge may execute
```

Any new commit invalidates old authorization.

### B. Workflow Automation

Adds:

- reusable Task Templates;
- Stage Templates;
- context packaging;
- repair-loop automation;
- handoff packets;
- workflow metrics;
- policy-driven retries for safe/idempotent operations.

FIX loop:

```text
Controller FIX
→ bounded repair packet
→ same role/runtime
→ new execution
→ new evidence
→ re-review
```

### C. Knowledge Plane + Obsidian Projection

After a stage closes:

```text
Evidence finalized
→ Controller decision recorded
→ repository state finalized
→ knowledge extraction
→ Project Memory / Engineering Knowledge / Research & Value Threads
→ Obsidian-compatible Markdown projection
```

Obsidian is the human knowledge interface. Möbius structured state remains authoritative.

Default synchronization:

```text
Möbius → Obsidian
```

Bidirectional editing requires a separate ADR.

### D. Hermes / Multi-Runtime Expansion Path

Möbius admits `HermesRuntime` only after dedicated integration research validates:

- invocation surface;
- persistence/context semantics;
- task identity;
- status/events;
- interrupt/recovery;
- permissions;
- artifact/evidence boundaries.

The runtime abstraction is capability-aware:

```text
AgentRuntime
├── CodexRuntime
├── HermesRuntime
└── FutureRuntime
```

Möbius never pretends two runtimes have identical semantics when they do not.

### v1.1 target experience

```text
You:
Continue FlowTracer.

Möbius:
Stage BE-7 admitted.
Backend resolved to CodexRuntime.
Workspace validated.
Frozen contract dispatched.
Execution completed.
Evidence collected.
PR opened; CI passed.
Controller review found one P2.
Repair loop completed.
Second review passed.
Exact-head merge authorization issued.
PR merged; worktrees synchronized.
Stage closed.
Project memory and Obsidian projection updated.
Next stage ready.
```

At this point Möbius is no longer merely a bridge. It is an executable AI software engineering operating system.

---

# 4. Failure Taxonomy / 故障分类

```text
F1 — Implementation defect
     → repair current stage

F2 — Runtime / compatibility defect
     → repair adapter / compatibility layer

F3 — Contract defect
     → Controller updates contract / ADR

F4 — Architectural invalidation
     → stop stage, explicit redesign, new architecture decision
```

Ordinary runtime or implementation defects must not silently churn the master architecture.

---

# 5. Documentation Authority / 文档权威

```text
00-PROJECT-CONTROL.md
        ↓
20-MOBIUS-MASTER-ARCHITECTURE-v1.md
        ↓
Architecture Amendments / ADRs
        ↓
11-VERSIONED-TECHNICAL-ROADMAP-v0.1-v1.1.md
        ↓
Stage Technical Design
        ↓
Task Contract
        ↓
Implementation
```

`10-MASTER-TECHNICAL-DESIGN.md` is the CodexRuntime implementation baseline inside this hierarchy.

---

# 6. Final Roadmap Principle / 最终路线原则

The target system is broad; implementation stays narrow.

We do not delay v0.1 to build Hermes, Git automation or Obsidian first. We prove the smallest real control loop, then expand it without sacrificing governance.

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**
