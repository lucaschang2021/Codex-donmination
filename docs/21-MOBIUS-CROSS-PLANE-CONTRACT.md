# Möbius Cross-Plane Contract v1

> Status: **Normative contract**
>
> This document defines authority, dependency, and data-flow boundaries between Möbius planes. Implementations may refine internals, but they must not silently violate these rules.

## 1. Plane authority

| Plane | Owns | Must not own |
|---|---|---|
| Architecture | Architecture contracts, dependency rules, module ownership, side-effect/state policy, architecture diff semantics | Runtime execution, merge authority |
| Governance | Stage admission, task admission, exceptions, PASS/FIX/BLOCK, risk acceptance, merge authorization | Provider-specific execution logic |
| Runtime | Agent discovery, bounded dispatch, status, interruption, result collection | Architecture policy, merge/release authority |
| Evidence | Mechanical facts and normalized validation records | Final architecture/risk judgment |
| Repository | Git/worktree/PR/CI mechanics and exact code state | Architecture exceptions, implicit release authority |
| Knowledge | Durable project memory, ADRs, lessons, human projection | Silent mutation of authoritative machine state |

## 2. Dependency direction

The product-level dependency direction is:

```text
Architecture Policy --------+
                            |
Governance -----------------+----> Application / Control Services
                            |                 |
Runtime Adapters -----------+                 +----> Evidence
                                              +----> Repository
                                              +----> Knowledge Projection
```

Rules:

1. Runtime adapters may expose capabilities, but they may not redefine governance policy.
2. Repository adapters may perform Git mechanics, but they may not infer merge authority from CI success.
3. Evidence collectors may report facts, but they may not turn findings into an architecture exception.
4. Knowledge projections may mirror approved state, but they may not become hidden configuration inputs.
5. Architecture policy must be consumable without importing runtime/provider internals.

## 3. Architecture Contract ownership

An Architecture Contract is owned by the Architecture Plane and admitted by Governance.

A contract version must include, at minimum:

- project identity;
- layer/module map;
- allowed and forbidden dependency directions;
- module responsibility statements;
- mutable-state ownership;
- side-effect policy;
- configuration ownership;
- public interface/versioning policy;
- complexity budgets or soft thresholds;
- required tests/gates;
- accepted exceptions and provenance.

Worker runtimes receive a snapshot. They do not edit the authoritative contract unless a separate governance-approved contract-change task is admitted.

## 4. Change contract

Every governed engineering change SHOULD carry:

```yaml
change:
  id: CHG-...
  project: ...
  architecture_contract_version: ...
  objective: ...
  non_goals: [...]
  allowed_files: [...]
  allowed_dependency_changes: [...]
  required_validation: [...]
  runtime: codex|claude|astra|hermes|...
  authority:
    may_implement: true
    may_change_architecture: false
    may_merge: false
```

A runtime may propose an architecture change, but proposal is not authority.

## 5. Plan Gate contract

Before execution, the Plan Gate must evaluate whether the proposed plan:

- targets modules consistent with declared responsibility;
- introduces forbidden cross-layer dependencies;
- expands scope beyond the admitted change;
- changes public interfaces without migration/versioning;
- requires new state ownership or side effects;
- exceeds declared complexity budgets without acknowledgment;
- depends on hidden environment/runtime assumptions.

Output:

```yaml
plan_gate:
  status: PASS|FIX|BLOCK|EXCEPTION_REQUIRED
  findings: [...]
```

## 6. Architecture Diff contract

After execution, the Architecture Plane computes a structured before/after delta.

Minimum fields:

```yaml
architecture_diff:
  dependency_edges_added: []
  dependency_edges_removed: []
  cross_layer_violations: []
  globals_added: []
  import_side_effects_added: []
  module_responsibility_expansion: []
  complexity_budget_changes: []
  public_interface_changes: []
  test_isolation_regressions: []
  state_ownership_changes: []
  contract_status: PASS|FIX|BLOCK|EXCEPTION_REQUIRED
```

## 7. Exception contract

Architecture exceptions are explicit governance objects.

```text
violation
  -> exception request
  -> evidence + rationale
  -> Controller/Governance decision
  -> scoped ADR / contract amendment
  -> exact version/scope
```

An exception must contain:

- violated rule;
- business/engineering rationale;
- alternatives considered;
- scope (files/modules/change IDs);
- expiry or review condition when appropriate;
- approving authority;
- resulting contract/ADR version.

## 8. Evidence contract

Evidence is appendable and machine-verifiable where possible.

Examples:

- Git diff/stat;
- test results;
- lint/type/build results;
- dependency graph delta;
- import-side-effect scan;
- complexity delta;
- runtime error state;
- CI status;
- PR head SHA;
- architecture-gate findings.

Evidence must distinguish fact from interpretation.

Example:

```yaml
evidence:
  fact: api_server imports mcp_server
  interpretation: adapter_to_adapter_coupling
  policy_rule: AG-DEP-003
```

## 9. Merge authority contract

A merge authorization binds to the exact reviewed repository state.

At minimum:

```yaml
merge_authorization:
  repository: owner/repo
  pr: 42
  reviewed_head_sha: abc123
  architecture_gate: PASS
  validation_manifest: ...
  approved_by: controller
```

If the PR head SHA changes, the authorization is invalid.

## 10. Knowledge contract

Knowledge Plane outputs are projections of approved state and learned context.

Allowed:

- ADR summaries;
- stage records;
- architecture debt history;
- recurring failure patterns;
- runtime compatibility notes;
- accepted exceptions;
- project lessons;
- Obsidian-compatible Markdown.

Not allowed:

- silently changing authoritative contract values;
- converting free-form notes into executable policy without admission;
- overriding repository/evidence state.

## 11. Self-governance rule

Möbius must govern its own development using the same contract model it exposes to other projects.

No internal subsystem is exempt from:

- declared responsibility;
- dependency direction;
- side-effect policy;
- evidence requirements;
- architecture diff;
- explicit exceptions.
