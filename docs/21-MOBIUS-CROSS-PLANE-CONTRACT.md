# Möbius — Cross-Plane System Contract / 跨控制平面系统契约

> Status: **Canonical Interface Contract / 规范接口契约**
>
> Purpose: define how the five Möbius control planes communicate without leaking authority or provider-specific details across boundaries.

---

## 1. Why This Contract Exists / 为什么需要这份契约

Möbius is intentionally split into five planes:

```text
Governance
Runtime
Evidence
Repository
Knowledge
```

The system remains coherent only if those planes exchange explicit typed state rather than implicit assumptions.

This document freezes the minimum cross-plane responsibilities for the target architecture. Implementation details may evolve, but no component may silently absorb another plane's authority.

---

## 2. Global Invariants / 全局不变量

1. **Controller authority is explicit.**
2. **Runtime capability does not imply governance authority.**
3. **Worker completion is a claim, not evidence.**
4. **Evidence is factual input, not final judgment.**
5. **Repository automation does not own merge approval.**
6. **Knowledge projection does not own runtime truth.**
7. **Exact identities are required for control-critical actions.**
8. **Every irreversible or high-authority action must be auditable.**
9. **Unsupported runtime semantics fail explicitly.**
10. **Architecture changes require explicit ADR treatment.**

---

## 3. Canonical Core Identities / 核心身份

```text
ProjectId
StageId
TaskId
RoleId
RuntimeId
AgentId
ExecutionId
WorkspaceId
RepositoryId
PullRequestId
EvidenceId
DecisionId
KnowledgeRecordId
```

IDs from upstream systems such as Codex thread IDs, Hermes agent/session IDs, Git SHAs and GitHub PR numbers are preserved as external identities and linked to Möbius internal identities.

No fuzzy matching is allowed for a write/control action.

---

## 4. Governance Plane Contract

### Inputs

- project configuration;
- frozen architecture/ADR state;
- stage definition;
- role bindings;
- task contract;
- evidence bundle;
- repository state;
- runtime capability report.

### Outputs

```text
StageAdmission
TaskAuthorization
ControllerDecision(PASS | FIX | BLOCK)
MergeAuthorization
NextStageAdmission
```

### Forbidden behavior

Governance must not fabricate runtime completion, Git state or validation results.

---

## 5. Runtime Plane Contract

### Required normalized capabilities

```text
discover()
read_context(agent_id)
attach(agent_id)
dispatch(agent_id, task_contract)
watch(execution_id)
interrupt(execution_id)
collect_result(execution_id)
capabilities()
```

### RuntimeCapabilitySet

A runtime declares supported semantics explicitly, for example:

```yaml
persistent_identity: true
structured_read: true
resume: true
live_status: true
interrupt: true
artifact_refs: true
approval_events: true
```

Möbius must never silently emulate an unsupported control-critical capability.

### Outputs

```text
AgentIdentity
ContextSnapshot
DispatchReceipt
ExecutionEvent
ExecutionState
RuntimeResult
RuntimeDiagnostic
```

### Forbidden behavior

Runtime implementations cannot self-admit stages, self-approve merge or mutate governance decisions.

---

## 6. Evidence Plane Contract

### Inputs

- TaskId / ExecutionId;
- workspace/repository identity;
- task acceptance criteria;
- validation profile;
- runtime result;
- repository/CI state.

### Output: ValidationManifest

Candidate schema:

```yaml
manifest_id: ev-...
project_id: ...
stage_id: ...
task_id: ...
execution_id: ...
workspace_id: ...
repository:
  base_sha: ...
  head_sha: ...
  changed_files: []
validation:
  tests: pass
  lint: pass
  typecheck: pass
  build: pass
ci:
  status: pass
contract_deviations: []
runtime_errors: []
generated_at: ...
```

### Forbidden behavior

Evidence Collector does not issue PASS/FIX/BLOCK. It reports facts and uncertainty.

---

## 7. Repository Plane Contract

### Read-side capabilities

```text
inspect_repository()
inspect_workspace()
get_branch_state()
get_diff()
get_pr_state()
get_ci_state()
```

### Write-side capabilities

```text
prepare_branch()
prepare_worktree()
commit()
push()
open_or_update_pr()
merge_authorized()
sync_after_merge()
```

### MergeAuthorization

A valid merge authorization must bind at minimum:

```yaml
project_id: ...
stage_id: ...
repository_id: ...
pull_request_id: ...
authorized_head_sha: ...
controller_decision_id: ...
issued_at: ...
```

Authorization becomes invalid when relevant repository state changes, especially PR head SHA.

### Forbidden behavior

The Repository Plane does not infer authorization from green CI, worker completion, PR mergeability or a prior PASS against a different head SHA.

---

## 8. Knowledge Plane Contract

### Inputs

Knowledge extraction may consume only finalized or provenance-tagged sources such as:

- architecture/ADR records;
- closed stage records;
- Controller decisions;
- Validation Manifests;
- final repository state;
- runtime compatibility findings;
- explicit research/value-thread records.

### Structured knowledge records

```text
ArchitectureDecision
StageRecord
ControllerDecisionRecord
FailureRecord
FixPattern
RuntimeCompatibilityFinding
EngineeringLesson
ResearchThread
ProductHypothesis
ValueThread
```

### Projection

```text
Structured Möbius knowledge
        ↓
Knowledge Projection Engine
        ↓
Obsidian-compatible Markdown
```

Every projected note should preserve provenance.

### Forbidden behavior

Obsidian edits do not automatically mutate Stage, Repository or Controller state. Bidirectional operation requires a separate ADR.

---

## 9. Task Contract / 任务契约

Canonical Task Contract fields:

```yaml
project_id: ...
stage_id: ...
task_id: ...
role_id: ...
runtime_id: ...
agent_id: ...
workspace_id: ...
objective: ...
frozen_scope: []
non_goals: []
allowed_paths: []
forbidden_actions: []
acceptance_criteria: []
validation_profile: ...
evidence_requirements: []
failure_rules: ...
report_format: ...
```

The Task Contract is the boundary between governance intent and runtime execution.

---

## 10. Stage Contract / 阶段契约

Canonical Stage state:

```text
PLANNED
ADMITTED
IMPLEMENTING
SUBMITTED
REVIEWING
FIX_REQUIRED
BLOCKED
PASS
MERGE_AUTHORIZED
MERGED
CLOSED
```

Transitions must be explicit and auditable.

Minimum transition examples:

```text
PLANNED → ADMITTED
requires Controller admission

SUBMITTED → REVIEWING
requires evidence package or explicit evidence waiver

REVIEWING → PASS/FIX/BLOCK
requires Controller decision

PASS → MERGE_AUTHORIZED
requires explicit merge authorization

MERGE_AUTHORIZED → MERGED
requires matching repository state

MERGED → CLOSED
requires finalized stage record
```

---

## 11. Repair Loop Contract / 修复闭环契约

```text
Controller FIX
      ↓
FixRequest references prior Task + Evidence + Decision
      ↓
new bounded repair Task
      ↓
same or explicitly reassigned Role
      ↓
new Execution
      ↓
new Evidence
      ↓
Controller re-review
```

Old evidence remains immutable; later evidence supersedes it by reference rather than deletion.

---

## 12. Knowledge Closure Contract / 知识闭环契约

A long-term stage closure should emit:

```text
StageRecord
ControllerDecisionRecord
FinalRepositoryState
FinalValidationManifest
KnowledgeExtractionResult
ProjectionResult
```

The next stage may consume prior knowledge, but knowledge suggestions do not override frozen architecture or stage contracts.

---

## 13. Multi-Runtime Contract / 多运行时契约

`CodexRuntime` is the reference implementation.

`HermesRuntime` is the first planned second implementation.

A new runtime is admitted only after:

```text
integration research
→ capability mapping
→ threat/permission review
→ adapter contract tests
→ real-environment validation
→ ADR
→ Controller admission
```

No provider is allowed to redefine the upper Möbius governance model simply because its native API is different.

---

## 14. Security & Audit Contract / 安全与审计契约

Every high-authority action should be attributable to:

```text
who/what requested it
which project/stage/task
which exact target identity
which repository state
which decision/evidence authorized it
when it occurred
what result occurred
```

Secrets and raw sensitive payloads must be excluded or redacted before entering evidence and knowledge projections.

---

## 15. Canonical End-to-End Contract

```text
Controller intent
→ StageAdmission
→ Role resolution
→ Runtime capability check
→ Repository workspace admission
→ TaskContract
→ DispatchReceipt
→ ExecutionEvents
→ RuntimeResult
→ ValidationManifest
→ ControllerDecision
→ optional FixRequest loop
→ MergeAuthorization(exact head SHA)
→ Repository merge
→ StageRecord CLOSED
→ Knowledge extraction
→ Obsidian projection
→ next-stage admission
```

This contract is the core systems boundary of Möbius.

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**
