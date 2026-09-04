"""Single composition root for Möbius dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from mobius.application.gate_service import ArchitectureGateService
from mobius.infrastructure.python_scanner import PythonRepositoryScanner


@dataclass(frozen=True, slots=True)
class Container:
    architecture_gate: ArchitectureGateService


def build_container() -> Container:
    scanner = PythonRepositoryScanner()
    return Container(architecture_gate=ArchitectureGateService(scanner=scanner))
