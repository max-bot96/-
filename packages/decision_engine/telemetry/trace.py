from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class StageTrace:
    name: str
    started_at: str = ""
    ended_at: str = ""
    duration_ms: float = 0.0
    success: bool = True
    error: str = ""


@dataclass
class PipelineTrace:
    stages: list[StageTrace] = field(default_factory=list)

    def start_stage(self, name: str) -> None:
        self.stages.append(
            StageTrace(
                name=name,
                started_at=datetime.now(UTC).isoformat(),
            )
        )

    def end_stage(self, name: str, success: bool = True, error: str = "") -> None:
        for stage in self.stages:
            if stage.name == name and not stage.ended_at:
                stage.ended_at = datetime.now(UTC).isoformat()
                stage.success = success
                stage.error = error
                break
