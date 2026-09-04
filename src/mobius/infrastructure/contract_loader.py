"""TOML loading for Architecture Contracts. Filesystem I/O stays in infrastructure."""

from __future__ import annotations

import tomllib
from pathlib import Path

from mobius.domain.contract_validation import validate_contract
from mobius.domain.models import ArchitectureContract, Constraints, ModuleRule


class TomlContractLoader:
    def load(self, path: Path) -> ArchitectureContract:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        modules = tuple(
            ModuleRule(
                name=item["name"],
                paths=tuple(item.get("paths", ())),
                responsibility=item.get("responsibility", ""),
                may_depend_on=tuple(item.get("may_depend_on", ())),
                forbidden_import_prefixes=tuple(item.get("forbidden_import_prefixes", ())),
                side_effects=item.get("side_effects", "forbidden"),
            )
            for item in data.get("modules", ())
        )
        raw_constraints = data.get("constraints", {})
        constraints = Constraints(
            forbid_module_mutable_state=raw_constraints.get(
                "forbid_module_mutable_state", True
            ),
            forbid_import_time_calls=raw_constraints.get("forbid_import_time_calls", True),
            max_file_lines_soft=raw_constraints.get("max_file_lines_soft", 500),
            max_file_lines_hard=raw_constraints.get("max_file_lines_hard", 900),
            core_requires_isolated_unit_tests=raw_constraints.get(
                "core_requires_isolated_unit_tests", True
            ),
            fake_external_providers_required=raw_constraints.get(
                "fake_external_providers_required", True
            ),
            architecture_gate_required=raw_constraints.get(
                "architecture_gate_required", True
            ),
        )
        contract = ArchitectureContract(
            schema_version=int(data["schema_version"]),
            project=str(data["project"]),
            architecture_version=int(data["architecture_version"]),
            modules=modules,
            constraints=constraints,
        )
        return validate_contract(contract)
