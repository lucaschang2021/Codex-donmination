from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from openai_codex import Codex


@dataclass(frozen=True, slots=True)
class ThreadSummary:
    """Small stable view of a Codex thread used by Codex Domination."""

    thread_id: str
    name: str | None = None
    cwd: str | None = None
    preview: str | None = None
    updated_at: int | str | None = None


class ThreadDiscoveryService:
    """Read-only adapter around the official Codex Python SDK."""

    def __init__(self, codex_factory: Callable[[], Any] = Codex) -> None:
        self._codex_factory = codex_factory

    def list_threads(self, *, limit: int | None = None) -> list[ThreadSummary]:
        """Discover persistent threads without resuming or mutating them."""
        with self._codex_factory() as codex:
            response = codex.thread_list(limit=limit)
        return normalize_thread_list_response(response)


def normalize_thread_list_response(response: Any) -> list[ThreadSummary]:
    """Normalize the SDK response while keeping the bridge decoupled from generated models."""
    payload = _to_mapping(response)
    rows = payload.get("data", [])
    if not isinstance(rows, Iterable) or isinstance(rows, (str, bytes, dict)):
        raise ValueError("Codex thread/list response field 'data' must be a list")

    normalized: list[ThreadSummary] = []
    for row in rows:
        item = _to_mapping(row)
        thread_id = item.get("id") or item.get("threadId") or item.get("thread_id")
        if not isinstance(thread_id, str) or not thread_id.strip():
            raise ValueError("Codex thread/list returned a thread without a valid id")

        normalized.append(
            ThreadSummary(
                thread_id=thread_id,
                name=_optional_str(item.get("name")),
                cwd=_optional_str(item.get("cwd")),
                preview=_optional_str(item.get("preview")),
                updated_at=item.get("updatedAt", item.get("updated_at")),
            )
        )

    return normalized


def _to_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        dumped = model_dump(by_alias=True, mode="json")
        if isinstance(dumped, dict):
            return dumped
    raise ValueError(f"Expected a mapping-like Codex SDK value, got {type(value).__name__}")


def _optional_str(value: Any) -> str | None:
    return value if isinstance(value, str) else None
