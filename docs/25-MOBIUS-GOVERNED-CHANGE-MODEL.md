# Möbius Governed Change Model v1

> Status: **Core object model**

Möbius governs a software engineering **Change**, not an Agent.

## 1. Change object

```yaml
change:
  id: CHG-...
  project: owner/repo
  objective: ...
  non_goals: [...]
  stage: ...
  architecture_contract_version: ...
  baseline_sha: ...
  target_branch: ...
  workspace: ...
  runtime: codex|claude|astra|hermes|human|mixed
  role: backend|frontend|integration|review|...
  permissions:
    allowed_files: [...]
    forbidden_files: [...]
    may_change_architecture: false
    may_merge: false
  plan: ...
  plan_gate: ...
  execution: ...
  evidence: ...
  architecture_diff: ...
  review: ...
  authority_decision: ...
```

## 2. Lifecycle

```text
PROPOSED
  -> ADMITTED
  -> PLANNED
  -> PLAN_CHECKED
  -> EXECUTING
  -> SUBMITTED
  -> VALIDATING
  -> ARCHITECTURE_REVIEW
  -> FIX | BLOCK | PASS | EXCEPTION_REQUIRED
  -> MERGE_AUTHORIZED
  -> MERGED
  -> CLOSED
```

## 3. Invariants

1. A Change is bound to an Architecture Contract snapshot.
2. Execution does not imply review approval.
3. Passing tests does not imply architecture approval.
4. A runtime cannot grant itself new permissions.
5. Architecture exceptions require explicit governance action.
6. Merge authorization binds to exact reviewed repository state.
7. If the reviewed head changes, authorization is invalidated.
8. Evidence is retained separately from final judgment.
9. Knowledge extraction happens after authoritative state is recorded.

## 4. Single-agent and multi-agent equivalence

The Change model is independent of execution topology.

```text
Change A -> Codex
Change B -> Claude Code
Change C -> Human developer
Change D -> Backend Agent + Review Agent + Integration Agent
```

All four are governed by the same contract/gate model.

This prevents multi-agent orchestration from becoming the core product abstraction.

## 5. Plan model

A plan should declare:

- modules/files to touch;
- expected dependency changes;
- interfaces/events/schemas affected;
- state ownership changes;
- side effects introduced/removed;
- migration requirements;
- tests to add/change;
- architecture exceptions requested;
- expected evidence.

## 6. Evidence model

Evidence should distinguish observed facts from policy interpretation.

```yaml
evidence_item:
  kind: dependency_edge
  observed: api_server -> mcp_server
  source: repository_scan
  reproducible: true

finding:
  rule: AC-DEP-001
  interpretation: adapter_to_adapter_coupling
  severity: P1
```

## 7. Review model

Review combines:

- behavioral evidence;
- architecture evidence;
- repository state;
- risk/context judgment.

Possible decisions:

```text
PASS
FIX
BLOCK
EXCEPTION_REQUIRED
```

## 8. Why Change is the core object

Agent-centric systems ask:

> Which agent should do the task?

Möbius asks first:

> What change is being authorized, under which architecture, evidence, permissions, and merge authority?

Only then does it choose an execution strategy.

That distinction is foundational to the product.
