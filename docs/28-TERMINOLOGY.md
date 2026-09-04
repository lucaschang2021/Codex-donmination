# Möbius Terminology

Use these terms consistently across future documentation and implementation.

- **Change** — the primary governed unit of software evolution.
- **Architecture Contract** — versioned machine-readable architecture policy for a project.
- **Change Contract** — bounded authorization for one engineering Change.
- **Plan Gate** — pre-execution architecture/policy check.
- **Architecture Gate** — post-change structural governance check.
- **Architecture Diff** — structured before/after architectural delta.
- **Evidence** — reproducible facts from repository, tests, CI, runtime, and scanners.
- **Finding** — policy interpretation of evidence.
- **Controller / Governance Authority** — entity authorized to admit stages, approve exceptions, and authorize merge.
- **EngineeringRuntime** — Codex, Claude Code, Astra, Hermes, human, or another execution runtime.
- **Execution Strategy** — single-agent, multi-agent, human, or mixed execution topology.
- **Architecture Exception** — explicit approved deviation from the current contract.
- **Exact-SHA Authorization** — merge authority bound to the exact reviewed repository state.

Avoid using **multi-agent orchestrator**, **Codex thread manager**, or **autonomous software factory** as the primary product definition.
