"""Pure validation for Architecture Contracts."""

from __future__ import annotations

from dataclasses import dataclass

from .models import ArchitectureContract


@dataclass(frozen=True, slots=True)
class ContractValidationError(ValueError):
    problems: tuple[str, ...]

    def __str__(self) -> str:
        return "invalid Architecture Contract: " + "; ".join(self.problems)


def validate_contract(contract: ArchitectureContract) -> ArchitectureContract:
    problems: list[str] = []
    if contract.schema_version != 1:
        problems.append(f"unsupported schema_version={contract.schema_version}")
    if not contract.project.strip():
        problems.append("project must be non-empty")
    if contract.architecture_version < 1:
        problems.append("architecture_version must be >= 1")
    if not contract.modules:
        problems.append("at least one module rule is required")

    names = [module.name for module in contract.modules]
    if len(names) != len(set(names)):
        problems.append("module names must be unique")

    known = set(names)
    for module in contract.modules:
        if not module.name.strip():
            problems.append("module name must be non-empty")
        if not module.paths:
            problems.append(f"module {module.name!r} must own at least one path")
        unknown_dependencies = sorted(set(module.may_depend_on) - known)
        if unknown_dependencies:
            problems.append(
                f"module {module.name!r} references unknown dependencies: "
                + ", ".join(unknown_dependencies)
            )

    constraints = contract.constraints
    if constraints.max_file_lines_soft < 1:
        problems.append("max_file_lines_soft must be >= 1")
    if constraints.max_file_lines_hard < constraints.max_file_lines_soft:
        problems.append("max_file_lines_hard must be >= max_file_lines_soft")

    if problems:
        raise ContractValidationError(tuple(problems))
    return contract
