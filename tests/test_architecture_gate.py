from pathlib import PurePosixPath

from mobius.domain.evaluator import evaluate_snapshot
from mobius.domain.models import ArchitectureContract, Constraints, GateStatus, ModuleRule, ModuleSnapshot


def _contract() -> ArchitectureContract:
    return ArchitectureContract(
        schema_version=1,
        project="test",
        architecture_version=1,
        modules=(
            ModuleRule(
                name="domain",
                paths=("src/mobius/domain",),
                responsibility="pure domain logic",
                forbidden_import_prefixes=("mobius.infrastructure",),
                side_effects="forbidden",
            ),
        ),
        constraints=Constraints(),
    )


def test_forbidden_import_is_fix() -> None:
    snapshot = ModuleSnapshot(
        path=PurePosixPath("src/mobius/domain/bad.py"),
        imports=("mobius.infrastructure.python_scanner",),
    )
    report = evaluate_snapshot(_contract(), snapshot)
    assert report.status is GateStatus.FIX
    assert report.findings[0].rule_id == "AC-DEP-001"


def test_clean_domain_module_passes() -> None:
    snapshot = ModuleSnapshot(
        path=PurePosixPath("src/mobius/domain/good.py"),
        imports=("dataclasses",),
        line_count=40,
    )
    report = evaluate_snapshot(_contract(), snapshot)
    assert report.status is GateStatus.PASS
    assert report.findings == ()


def test_mutable_global_is_fix() -> None:
    snapshot = ModuleSnapshot(
        path=PurePosixPath("src/mobius/domain/state.py"),
        mutable_globals=("CACHE",),
    )
    report = evaluate_snapshot(_contract(), snapshot)
    assert report.status is GateStatus.FIX
    assert report.findings[0].rule_id == "AC-STATE-001"
