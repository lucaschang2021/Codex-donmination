# Möbius — Checkpoint & Recovery Architecture / 断点与恢复架构

> Status: **Reliability Architecture Amendment / 可靠性架构修正案**
>
> Scope: quota exhaustion, runtime interruption, process crash, transport loss, host restart, and other recoverable execution interruptions.

---

## 1. Thesis / 核心命题

Möbius must not depend on an agent remembering where it stopped.

**The system protects engineering state, not model memory.**

莫比乌斯不依赖 Agent “记得自己做到哪里”。真正需要保护的是：任务契约、仓库状态、已完成步骤、当前步骤、验证结果、运行时身份与最后一个可信断点。

Canonical rule:

> **If the runtime disappears, the task must remain reconstructable from durable evidence.**
>
> **即使 Runtime 消失，任务也必须能从持久化工程证据中重建。**

---

## 2. Architectural Position / 架构位置

Checkpoint & Recovery is a **cross-cutting reliability subsystem**, not a sixth independent control plane.

It spans:

```text
Governance Plane   → task/stage contract + recovery authority
Runtime Plane      → interruption detection + reattachment
Evidence Plane     → durable task/checkpoint evidence
Repository Plane   → exact Git/worktree state
Knowledge Plane    → reusable failure/recovery lessons
```

The five-plane Möbius architecture remains unchanged.

---

## 3. Failure Classes Covered / 覆盖的中断类型

```text
Q1 — QUOTA_EXHAUSTED
     Codex/runtime quota or usage limit interrupts work.

Q2 — RUNTIME_DISCONNECTED
     App Server / agent runtime / transport disappears.

Q3 — PROCESS_CRASHED
     Worker process or local orchestration process exits unexpectedly.

Q4 — HOST_RESTARTED
     Machine restart, sleep/wake failure, update, power loss.

Q5 — TURN_INTERRUPTED
     Active agent turn terminates before task completion.

Q6 — CONTROLLER_LOST
     Controller session disappears while worker/repository state persists.

Q7 — UNKNOWN_INTERRUPTION
     Cause cannot be identified safely.
```

Unknown interruption is never treated as successful completion.

---

## 4. Task Lifecycle Extension / 任务生命周期扩展

Möbius extends task execution state with explicit checkpoint/recovery states:

```text
ACCEPTED
   ↓
RUNNING
   ↓
CHECKPOINTED  ←──────────────┐
   ↓                         │
RUNNING                      │
   │                         │
   ├── COMPLETED             │
   ├── FAILED                │
   └── INTERRUPTED_*         │
          ↓                  │
      RECOVERY_PENDING       │
          ↓                  │
       RECOVERING            │
          ↓                  │
   RECOVERY_VERIFIED ────────┘
```

Special interruption labels may include:

```text
INTERRUPTED_QUOTA
INTERRUPTED_RUNTIME
INTERRUPTED_HOST
INTERRUPTED_TRANSPORT
INTERRUPTED_UNKNOWN
```

A recovered task re-enters `RUNNING` only after repository/task consistency is verified.

---

## 5. Durable Checkpoint / 持久化断点

A checkpoint is a structured engineering snapshot, not a free-form agent summary.

Candidate schema:

```yaml
checkpoint_id: cp_BE-5B_004
project_id: flowtracer
stage_id: BE-5
subtask_id: BE-5B
role: backend
runtime: codex
runtime_identity: <thread-or-agent-id>
status: CHECKPOINTED

contract_hash: <hash>
architecture_ref: <version-or-commit>

repository:
  repo: <repo>
  branch: feat/be-5
  worktree: <path>
  head_sha: <sha>
  last_good_commit: <sha>
  dirty: true
  diff_hash: <hash>

progress:
  completed:
    - database model
    - migration
    - model tests
  current:
    - implement update service
  remaining:
    - API endpoint
    - integration tests

validation:
  pytest: pass
  ruff: pass
  mypy: unknown

modified_files:
  - backend/models/example.py
  - backend/services/example.py

known_risks:
  - update path not integration-tested

created_at: <timestamp>
```

The exact storage format may evolve; the semantic fields are the important contract.

---

## 6. Checkpoint Creation Policy / 断点生成策略

Checkpointing should happen at **safe engineering boundaries**, not blindly every few seconds.

Recommended triggers:

```text
A. after a meaningful implementation unit completes
B. after targeted tests pass
C. after a checkpoint commit
D. before a risky migration/refactor
E. before starting a long-running task when quota is low
F. when runtime reports usage/quota risk, if observable
G. before Controller or host shutdown
H. periodically for long tasks, but only when state can be made consistent
```

Preferred sequence:

```text
implement small unit
→ validate
→ checkpoint commit or durable diff snapshot
→ write checkpoint record
→ continue
```

A checkpoint marked `verified=true` must reference reproducible repository state.

---

## 7. Recovery Protocol / 恢复协议

Möbius must never recover by simply telling a new agent: “continue”.

Canonical recovery sequence:

```text
1. Load frozen Task Contract.
2. Load latest valid checkpoint.
3. Resolve exact project / role / runtime identity.
4. Inspect repository, branch and worktree.
5. Verify HEAD against checkpoint.
6. Inspect dirty diff and compare diff hash when available.
7. Run targeted validation required by the checkpoint.
8. Reconstruct completed/current/remaining work.
9. Detect divergence or unknown mutations.
10. Produce Recovery Report.
11. Controller/policy verifies recovery safety.
12. Only then resume bounded execution.
```

Recovery report example:

```yaml
recovery:
  checkpoint: cp_BE-5B_004
  repository_match: true
  dirty_diff_match: true
  targeted_tests: pass
  contract_match: true
  unknown_changes: false
  safe_to_resume: true
```

If any critical invariant fails, state becomes `RECOVERY_BLOCKED` rather than guessing.

---

## 8. Repository Safety / Git 保护

Git is the primary durable recovery anchor.

Rules:

1. Prefer small checkpoint commits at meaningful safe boundaries.
2. Never auto-discard a dirty worktree during recovery.
3. Never reset/rebase automatically just to make checkpoint metadata match.
4. A `last_good_commit` is evidence, not permission to destroy later uncommitted work.
5. Dirty diff must be inspected and preserved before any repair action.
6. If repository state diverged after interruption, Controller sees the divergence explicitly.
7. Merge authorization remains invalid after any unreviewed state mutation.

Checkpointing therefore complements Repository Control; it does not bypass Git authority rules.

---

## 9. Quota-Aware Execution Policy / 额度感知策略

When runtime quota information is available, Möbius may use it as scheduling evidence.

Suggested policy profile:

```text
NORMAL        > 40% remaining
              ordinary bounded implementation

CAUTION       20–40%
              smaller task packets + more frequent safe checkpoints

CONSERVE      10–20%
              prefer tests, review, docs, evidence, checkpoint commits
              avoid starting large implementation units

DRAIN          <10%
              do not admit new long-running implementation
              finalize checkpoint and stop safely
```

These thresholds are configurable policy defaults, not universal truths.

If quota cannot be observed reliably, Möbius must not invent it. Manual Controller input remains valid.

---

## 10. Task Packet Requirements / Task Contract 新要求

Long-running Task Contracts should declare recovery metadata:

```text
checkpoint_policy
safe_checkpoint_boundaries
maximum_uncheckpointed_work
recovery_validation
non-idempotent_operations
repository_recovery_policy
runtime_resume_strategy
```

Tasks containing non-idempotent operations require special recovery treatment. Möbius must not blindly replay them.

Examples:

```text
external API mutation
production deployment
database destructive migration
billing action
release publication
```

---

## 11. Recovery Authority / 恢复权限

Recovery is not automatically equivalent to permission to continue.

```text
Mechanical reconstruction → may be automated
Repository verification    → may be automated
Targeted tests             → may be automated
Safe resume decision       → policy/Controller governed
Architecture deviation     → Controller required
Destructive repair         → explicit authorization required
```

A recovered worker retains exactly the authority of the original Task Contract—never more.

---

## 12. Knowledge Integration / 知识沉淀

Repeated interruption/recovery behavior becomes organizational knowledge.

Potential knowledge records:

```text
RecoveryIncident
RecoveryPattern
RuntimeQuotaFinding
CheckpointFailure
CheckpointPolicyAdjustment
RuntimeCompatibilityFinding
```

Obsidian projection may summarize meaningful incidents, but routine successful checkpoints should not flood the human knowledge base.

Example human note:

```text
Runtime: Codex
Project: FlowTracer
Stage: BE-5
Incident: quota interruption
Recovered from: cp_BE-5B_004
Repository divergence: none
Recovery validation: passed
Reusable lesson: split service implementation before integration tests
```

---

## 13. Version Admission / 版本落位

Checkpoint & Recovery should enter Möbius incrementally:

```text
v0.4  task identity and bounded dispatch provide recovery addressability
v0.5  interruption states + terminal/non-terminal lifecycle semantics
v0.6  durable checkpoint/evidence schema + recovery report prototype
v0.7  role/project/worktree-aware checkpoint binding
v0.8  Stage Gate recovery policy + Controller authority
v0.9  MCP recovery/status primitives
v1.0  reliable Codex-first interrupted-task recovery
v1.1  quota-aware scheduling, automated checkpoint policy, cross-runtime recovery
```

Hermes and future runtimes must map their own interruption/recovery semantics into the normalized recovery contract.

---

## 14. Candidate Control Surface / 候选控制接口

```text
checkpoint.create(task_id)
checkpoint.latest(task_id)
checkpoint.verify(checkpoint_id)
recovery.inspect(task_id)
recovery.report(task_id)
recovery.resume(task_id)
recovery.abort(task_id)
```

`recovery.resume()` must enforce Task Contract and Stage Gate authority. It is not a generic “run again” primitive.

---

## 15. Definition of Success / 成功标准

Möbius has solved interrupted execution when this scenario is routine rather than catastrophic:

```text
Codex is implementing BE-5B
        ↓
quota is exhausted / runtime disappears
        ↓
Möbius records INTERRUPTED_QUOTA
        ↓
latest durable checkpoint remains available
        ↓
quota/runtime becomes available again
        ↓
Möbius verifies contract + Git + diff + tests
        ↓
Recovery Report says SAFE_TO_RESUME
        ↓
exact role/runtime receives reconstructed bounded context
        ↓
work continues without guessing or losing completed engineering state
```

Final principle:

> **Do not protect the agent's memory. Protect the engineering state.**
>
> **不要保护 Agent 的记忆，要保护工程状态。**
