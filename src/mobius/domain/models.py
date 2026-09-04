"""Pure domain models for architecture governance."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import PurePosixPath


class Severity(StrEnum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class GateStatus(StrEnum):
    PASS = "PASS"
    FIX = "FIX"
    BLOCK = "BLOCK"


@dataclass(frozen=True, slots=True)
class ModuleRule:
    name: str
    paths: tuple[str, ...]
    responsibility: str
    may_depend_on: tuple[str, ...] = ()
    forbidden_import_prefixes: tuple[str, ...] = ()
    side_effects: str = "forbidden"

    def owns(self, path: PurePosixPath) -> bool:
        text = path.as_posix()
        return any(
            text == prefix or text.startswith(prefix.rstrip("/") + "/")
            for prefix in self.paths
        )


@dataclass(frozen=True, slots=True)
class Constraints:
    forbid_module_mutable_state: bool = True
    forbid_import_time_calls: bool = True
    max_file_lines_soft: int = 500
    max_file_lines_hard: int = 900
    core_requires_isolated_unit_tests: bool = True
    fake_external_providers_required: bool = True
    architecture_gate_required: bool = True


@dataclass(frozen=True, slots=True)
class ArchitectureContract:
    schema_version: int
    project: str
    architecture_version: int
    modules: tuple[ModuleRule, ...]
    constraints: Constraints

    def rule_for(self, path: PurePosixPath) -> ModuleRule | None:
        return next((rule for rule in self.modules if rule.owns(path)), None)


@dataclass(frozen=True, slots=True)
class ModuleSnapshot:
    path: PurePosixPath
    imports: tuple[str, ...] = ()
    mutable_globals: tuple[str, ...] = ()
    import_time_calls: tuple[str, ...] = ()
    line_count: int = 0


@dataclass(frozen=True, slots=True)
class Finding:
    rule_id: str
    severity: Severity
    path: str
    evidence: str
    remediation: str


@dataclass(frozen=True, slots=True)
class GateReport:
    status: GateStatus
    findings: tuple[Finding, ...] = field(default_factory=tuple)

    @property
    def blocking(self) -> tuple[Finding, ...]:
        return tuple(f for f in self.findings if f.severity in {Severity.P0, Severity.P1})
