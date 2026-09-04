# Möbius Reference Project Governance Policies

> Status: **Reference policy pack**

This document turns real architecture findings from FinTerminal, FlowTracer, and Gallop into reusable Möbius governance patterns. These are reference contracts, not universal rules.

## 1. FinTerminal policy profile

### Objective

Reduce structural coupling while preserving the working product through incremental refactoring.

### High-priority rules

```yaml
profile: finterminal
legacy_policy: no_regression

rules:
  adapter_to_adapter_dependency: forbidden
  entrypoint_as_business_kernel: forbidden
  import_time_plugin_loading: forbidden
  hidden_runtime_globals: forbidden
  core_requires_transport_startup: forbidden
```

### Expected detections

- REST/desktop adapter imports MCP entrypoint and calls internal business functions through it.
- Entry point owns model selection, configuration, session persistence, plugin loading, and application orchestration simultaneously.
- Importing path/config/plugin modules mutates filesystem or registries.
- Core logic cannot be tested without MCP/FastAPI/provider/keyring initialization.

### Preferred remediation

```text
adapter -> application service <- adapter
                    |
                 domain/ports
                    |
              infrastructure
```

Use strangler extraction. Do not rewrite the product wholesale.

## 2. FlowTracer policy profile

### Objective

Preserve the existing modular backend while detecting service growth before it becomes structural debt.

### High-priority rules

```yaml
profile: flowtracer

rules:
  application_entrypoint: bootstrap_only
  typed_settings: required
  provider_substitutability: required
  fake_provider_for_core_tests: required
  import_time_external_io: forbidden

soft_budgets:
  acquisition_service_responsibility_growth: warn
  intelligence_service_responsibility_growth: warn
```

### Protected patterns

- `create_app(...)` remains composition/bootstrap.
- Database/Redis/provider initialization occurs in explicit lifecycle code.
- API dependencies remain explicit.
- External AI/embedding providers remain replaceable by fakes.
- Core/service tests do not require paid external APIs.

### Warning pattern

Large services such as acquisition/intelligence may remain valid orchestration modules, but Möbius should warn when dependency count, responsibilities, or file growth indicate emerging God-service risk.

## 3. Gallop policy profile

### Objective

Preserve deterministic evidence/progression authority while RC2 and future mentorship logic expand.

### High-priority rules

```yaml
profile: gallop

rules:
  event_journal_authority: required
  deterministic_domain_engine_side_effects: forbidden
  provider_output_as_mastery_authority: forbidden
  orchestration_service_domain_decisions: forbidden
  progressive_mentorship_engine_isolation: required
```

### Protected patterns

- Evidence -> replay -> derived state remains deterministic.
- Mastery/progression rules accept explicit inputs and return explicit outputs.
- DeepTutor/provider output is preparation/evidence input, not mastery authority.
- `automation/service.py` coordinates storage, lifecycle, adapters, and human confirmation.

### RC2 architecture rule

The following decisions should live in dedicated deterministic engines/modules rather than accumulating inside `Automation`:

- Current Capability;
- Target Capability;
- Training Zone;
- Scaffolding;
- Productive Struggle classification;
- prerequisite diagnosis;
- Capability Gain;
- Mentor Role;
- Research Independence.

## 4. Policy-template extraction

These project-specific rules should later generalize into templates:

```text
legacy-modularization
bootstrap-only-entrypoint
provider-substitutability
deterministic-domain-core
orchestration-only-service
no-adapter-to-adapter
no-import-side-effects
explicit-state-ownership
```

A project opts into or overrides templates through its Architecture Contract.

## 5. Validation purpose

Möbius should continuously test itself against these three projects because they represent different architecture conditions:

- **FinTerminal:** existing architecture debt and incremental remediation;
- **FlowTracer:** relatively healthy modular backend requiring drift prevention;
- **Gallop:** deterministic domain architecture requiring boundary preservation during rapid feature expansion.

If Möbius cannot explain and govern these three cases deterministically enough to be useful, its architecture-governance thesis is not yet proven.
