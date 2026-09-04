"""Deterministic architecture-rule evaluation with no I/O."""

from __future__ import annotations

from .models import ArchitectureContract, Finding, GateReport, GateStatus, ModuleSnapshot, Severity


def evaluate_snapshot(contract: ArchitectureContract, snapshot: ModuleSnapshot) -> GateReport:
    findings: list[Finding] = []
    rule = contract.rule_for(snapshot.path)
    if rule is None:
        return GateReport(status=GateStatus.PASS)

    for imported in snapshot.imports:
        forbidden = any(
            imported == prefix or imported.startswith(prefix + ".")
            for prefix in rule.forbidden_import_prefixes
        )
        if forbidden:
            findings.append(
                Finding(
                    rule_id="AC-DEP-001",
                    severity=Severity.P1,
                    path=snapshot.path.as_posix(),
                    evidence=f"forbidden import: {imported}",
                    remediation=(
                        "depend on an allowed port/application boundary "
                        "or move the responsibility"
                    ),
                )
            )

    if contract.constraints.forbid_module_mutable_state:
        for name in snapshot.mutable_globals:
            findings.append(
                Finding(
                    rule_id="AC-STATE-001",
                    severity=Severity.P1,
                    path=snapshot.path.as_posix(),
                    evidence=f"module-level mutable state: {name}",
                    remediation="move mutable runtime state behind an explicit owner and lifecycle",
                )
            )

    if contract.constraints.forbid_import_time_calls and rule.side_effects == "forbidden":
        for call in snapshot.import_time_calls:
            findings.append(
                Finding(
                    rule_id="AC-SIDE-001",
                    severity=Severity.P1,
                    path=snapshot.path.as_posix(),
                    evidence=f"top-level call in side-effect-free module: {call}",
                    remediation="move runtime work to bootstrap or an explicit method",
                )
            )

    if snapshot.line_count > contract.constraints.max_file_lines_hard:
        findings.append(
            Finding(
                rule_id="AC-CPLX-002",
                severity=Severity.P1,
                path=snapshot.path.as_posix(),
                evidence=(
                    f"file has {snapshot.line_count} lines; hard limit is "
                    f"{contract.constraints.max_file_lines_hard}"
                ),
                remediation="split responsibilities before adding more behavior",
            )
        )
    elif snapshot.line_count > contract.constraints.max_file_lines_soft:
        findings.append(
            Finding(
                rule_id="AC-CPLX-001",
                severity=Severity.P2,
                path=snapshot.path.as_posix(),
                evidence=(
                    f"file has {snapshot.line_count} lines; soft limit is "
                    f"{contract.constraints.max_file_lines_soft}"
                ),
                remediation="review responsibility growth and consider extraction",
            )
        )

    if any(f.severity is Severity.P0 for f in findings):
        status = GateStatus.BLOCK
    elif any(f.severity is Severity.P1 for f in findings):
        status = GateStatus.FIX
    else:
        status = GateStatus.PASS
    return GateReport(status=status, findings=tuple(findings))


def evaluate_repository(
    contract: ArchitectureContract,
    snapshots: tuple[ModuleSnapshot, ...],
) -> GateReport:
    findings = tuple(
        finding
        for snapshot in snapshots
        for finding in evaluate_snapshot(contract, snapshot).findings
    )
    if any(f.severity is Severity.P0 for f in findings):
        status = GateStatus.BLOCK
    elif any(f.severity is Severity.P1 for f in findings):
        status = GateStatus.FIX
    else:
        status = GateStatus.PASS
    return GateReport(status=status, findings=findings)
