from __future__ import annotations

from packages.decision_engine.interfaces.protocols import Stage


class StageRegistry:
    """Registry for pipeline stages. Supports insert, remove, and replace."""

    def __init__(self) -> None:
        self._stages: dict[str, Stage] = {}
        self._order: list[str] = []

    def register(self, name: str, stage: Stage) -> None:
        self._stages[name] = stage
        if name not in self._order:
            self._order.append(name)

    def insert_after(self, after: str, name: str, stage: Stage) -> None:
        self._stages[name] = stage
        idx = self._order.index(after) + 1 if after in self._order else len(self._order)
        self._order.insert(idx, name)

    def insert_before(self, before: str, name: str, stage: Stage) -> None:
        self._stages[name] = stage
        idx = self._order.index(before) if before in self._order else 0
        self._order.insert(idx, name)

    def remove(self, name: str) -> None:
        self._stages.pop(name, None)
        if name in self._order:
            self._order.remove(name)

    def replace(self, name: str, stage: Stage) -> None:
        self._stages[name] = stage

    def get(self, name: str) -> Stage | None:
        return self._stages.get(name)

    @property
    def ordered_stages(self) -> list[Stage]:
        return [self._stages[name] for name in self._order if name in self._stages]
