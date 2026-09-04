from pathlib import Path, PurePosixPath

from mobius.application.gate_service import ArchitectureGateService
from mobius.domain.models import (
    ArchitectureContract,
    Constraints,
    GateStatus,
    ModuleRule,
    ModuleSnapshot,
)


class FakeScanner:
    def __init__(self, snapshots: tuple[ModuleSnapshot, ...]) -> None:
        self._snapshots = snapshots

    def scan(self, root: Path) -> tuple[ModuleSnapshot, ...]:
        del root
        return self._snapshots


def test_application_service_does_not_require_real_filesystem_scanner() -> None:
    contract = ArchitectureContract(
        schema_version=1,
        project="test",
        architecture_version=1,
        modules=(
            ModuleRule(
                name="domain",
                paths=("src/domain",),
                responsibility="pure rules",
                forbidden_import_prefixes=("infra",),
            ),
        ),
        constraints=Constraints(),
    )
    scanner = FakeScanner(
        (
            ModuleSnapshot(
                path=PurePosixPath("src/domain/rules.py"),
                imports=("infra.db",),
            ),
        )
    )

    report = ArchitectureGateService(scanner=scanner).evaluate(
        root=Path("unused"),
        contract=contract,
    )

    assert report.status is GateStatus.FIX
    assert report.findings[0].rule_id == "AC-DEP-001"
