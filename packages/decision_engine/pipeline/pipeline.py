from __future__ import annotations

from packages.decision_engine.contracts.models import (
    Decision,
    DecisionRequest,
    DecisionResult,
    DecisionStatus,
)
from packages.decision_engine.pipeline.context import PipelineContext
from packages.decision_engine.registry.registry import StageRegistry


class DecisionPipeline:
    """Middleware-style pipeline for decision processing."""

    def __init__(self, registry: StageRegistry) -> None:
        self._registry = registry

    async def execute(self, request: DecisionRequest) -> DecisionResult:
        context = PipelineContext(request=request)

        for stage in self._registry.ordered_stages:
            try:
                context = await stage.process(context)
            except Exception as e:
                context = context.with_error(str(e))

        if context.result is not None:
            return context.result

        return DecisionResult(
            request_id=request.request_id,
            decision=Decision(status=DecisionStatus.failed),
        )
