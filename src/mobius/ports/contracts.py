"""Application-owned port for Architecture Contract loading."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from mobius.domain.models import ArchitectureContract


class ContractLoader(Protocol):
    def load(self, path: Path) -> ArchitectureContract: ...
