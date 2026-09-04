"""Application-owned ports for repository inspection."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from mobius.domain.models import ModuleSnapshot


class RepositoryScanner(Protocol):
    def scan(self, root: Path) -> tuple[ModuleSnapshot, ...]: ...
