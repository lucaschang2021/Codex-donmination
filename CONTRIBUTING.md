# Contributing to Möbius

Möbius governs software change, so changes to Möbius itself must follow the same rules.

## 1. Read the architecture before editing

Required reading for non-trivial changes:

- `ARCHITECTURE.toml`
- `docs/20-MOBIUS-MASTER-ARCHITECTURE-v1.md`
- `docs/21-MOBIUS-ARCHITECTURE-CONTRACT.md`
- `docs/23-ARCHITECTURE-GATE-SPEC.md`
- `docs/29-MOBIUS-SELF-GOVERNANCE.md`

## 2. Dependency direction

The intended code dependency direction is:

```text
adapters -> bootstrap -> application -> domain
                         |             ^
                         v             |
                        ports <--- infrastructure
```

More precisely:

- `domain/` contains deterministic governance models and rules and performs no I/O.
- `ports/` contains abstract boundaries owned by the application/domain side.
- `application/` orchestrates use cases through ports; it does not import concrete infrastructure.
- `infrastructure/` implements ports and owns filesystem/network/process/provider integration.
- `adapters/` translate CLI/API/MCP input/output and must not become business kernels.
- `bootstrap.py` is the single composition root that wires concrete dependencies.

`ARCHITECTURE.toml` is the machine-readable authority when examples and prose disagree.

## 3. Change rules

Do not:

- add hidden module-global runtime state;
- perform network/filesystem/process/plugin work during import;
- put domain decisions in CLI/API/MCP handlers;
- let an adapter import concrete infrastructure directly;
- make core tests require real external services when a port/fake is appropriate;
- weaken an Architecture Contract in the same change merely to make a violation pass.

If the architecture itself must change, propose the architecture change explicitly and version the contract.

## 4. Required local checks

```bash
python -m pip install -e '.[dev]'
ruff check src tests
mypy src
pytest
mobius gate . --contract ARCHITECTURE.toml
```

## 5. Pull request evidence

A non-trivial PR should state:

- objective and non-goals;
- modules/interfaces touched;
- behavior evidence (tests/lint/types/build as applicable);
- architecture evidence (gate result and relevant dependency/state/side-effect changes);
- migrations or compatibility impact;
- unresolved P2/P3 debt;
- whether the Architecture Contract or an ADR changes.

Passing tests do not waive architecture findings. Passing the Architecture Gate does not prove behavioral correctness.

## 6. Authority

Implementation agents and contributors may propose fixes, plans, and contract changes. They may not silently waive violations, redefine merge authority, or treat their own completion report as approval.
