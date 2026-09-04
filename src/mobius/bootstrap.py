"""Single composition root for Möbius dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from mobius.application.gate_service import ArchitectureGateService
from mobius.infrastructure.contract_loader import TomlContractLoader
from mobius.infrastructure.python_scanner import PythonRepositoryScanner
from mobius.ports.contracts import ContractLoader


@dataclass(frozen=True, slots=True)
class Container:
    architecture_gate: ArchitectureGateService
    contract_loader: ContractLoader


def build_container() -> Container:
    scanner = PythonRepositoryScanner()
    contract_loader = TomlContractLoader()
    return Container(
        architecture_gate=ArchitectureGateService(scanner=scanner),
        contract_loader=contract_loader,
    )
