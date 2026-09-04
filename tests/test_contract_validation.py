import pytest

from mobius.domain.contract_validation import ContractValidationError, validate_contract
from mobius.domain.models import ArchitectureContract, Constraints, ModuleRule


def test_unknown_module_dependency_is_rejected() -> None:
    contract = ArchitectureContract(
        schema_version=1,
        project="demo",
        architecture_version=1,
        modules=(
            ModuleRule(
                name="domain",
                paths=("src/demo/domain",),
                responsibility="rules",
                may_depend_on=("missing",),
            ),
        ),
        constraints=Constraints(),
    )

    with pytest.raises(ContractValidationError, match="unknown dependencies"):
        validate_contract(contract)


def test_hard_limit_cannot_be_lower_than_soft_limit() -> None:
    contract = ArchitectureContract(
        schema_version=1,
        project="demo",
        architecture_version=1,
        modules=(
            ModuleRule(
                name="domain",
                paths=("src/demo/domain",),
                responsibility="rules",
            ),
        ),
        constraints=Constraints(max_file_lines_soft=500, max_file_lines_hard=400),
    )

    with pytest.raises(ContractValidationError, match="max_file_lines_hard"):
        validate_contract(contract)
