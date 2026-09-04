"""Static Python repository scanning. No imports or execution of target code."""

from __future__ import annotations

import ast
from pathlib import Path, PurePosixPath

from mobius.domain.models import ModuleSnapshot

_MUTABLE_LITERALS = (ast.List, ast.Dict, ast.Set)
_SAFE_TOP_LEVEL_CALLS = frozenset(
    {"dataclass", "field", "tuple", "frozenset", "Path", "PurePosixPath"}
)


def _call_name(call: ast.Call) -> str:
    target = call.func
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        parts: list[str] = [target.attr]
        value = target.value
        while isinstance(value, ast.Attribute):
            parts.append(value.attr)
            value = value.value
        if isinstance(value, ast.Name):
            parts.append(value.id)
        return ".".join(reversed(parts))
    return "<dynamic-call>"


def _imports(tree: ast.Module) -> tuple[str, ...]:
    values: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            values.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            values.add(node.module)
    return tuple(sorted(values))


def _mutable_globals(tree: ast.Module) -> tuple[str, ...]:
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, _MUTABLE_LITERALS):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and isinstance(node.value, _MUTABLE_LITERALS)
        ):
            names.add(node.target.id)
    return tuple(sorted(names))


def _top_level_calls(tree: ast.Module) -> tuple[str, ...]:
    calls: set[str] = set()
    for node in tree.body:
        candidate: ast.Call | None = None
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            candidate = node.value
        elif isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(node.value, ast.Call):
            candidate = node.value
        if candidate is None:
            continue
        name = _call_name(candidate)
        if name.rsplit(".", 1)[-1] not in _SAFE_TOP_LEVEL_CALLS:
            calls.add(name)
    return tuple(sorted(calls))


def scan_python_file(root: Path, path: Path) -> ModuleSnapshot:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    relative = PurePosixPath(path.relative_to(root).as_posix())
    return ModuleSnapshot(
        path=relative,
        imports=_imports(tree),
        mutable_globals=_mutable_globals(tree),
        import_time_calls=_top_level_calls(tree),
        line_count=len(source.splitlines()),
    )


class PythonRepositoryScanner:
    """Filesystem adapter implementing the RepositoryScanner port."""

    def scan(self, root: Path) -> tuple[ModuleSnapshot, ...]:
        files = sorted(
            path
            for path in root.rglob("*.py")
            if ".git" not in path.parts and ".venv" not in path.parts
        )
        return tuple(scan_python_file(root, path) for path in files)
