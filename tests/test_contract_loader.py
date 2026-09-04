from pathlib import Path

from mobius.infrastructure.contract_loader import TomlContractLoader


def test_loads_minimal_contract(tmp_path: Path) -> None:
    path = tmp_path / "ARCHITECTURE.toml"
    path.write_text(
        """
schema_version = 1
project = "demo"
architecture_version = 2

[[modules]]
name = "domain"
paths = ["src/demo/domain"]
responsibility = "pure rules"
may_depend_on = []
forbidden_import_prefixes = ["demo.infrastructure"]
side_effects = "forbidden"

[constraints]
forbid_module_mutable_state = true
forbid_import_time_calls = true
max_file_lines_soft = 300
max_file_lines_hard = 600
""".strip(),
        encoding="utf-8",
    )

    contract = TomlContractLoader().load(path)

    assert contract.project == "demo"
    assert contract.architecture_version == 2
    assert contract.modules[0].name == "domain"
    assert contract.constraints.max_file_lines_soft == 300
