"""Application orchestration for architecture-gate execution."""

from __future__ import annotations

from pathlib import Path

from mobius.domain.evaluator import evaluate_repository
from mobius.domain.models import ArchitectureContract, GateReport
from mobius.ports.repository import RepositoryScanner


class ArchitectureGateService:
    def __init__(self, scanner: RepositoryScanner) -> None:
        self._scanner = scanner

    def evaluate(self, *, root: Path, contract: ArchitectureContract) -> GateReport:
        snapshots = self._scanner.scan(root)
        return evaluate_repository(contract, snapshots)
