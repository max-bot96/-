"""Demo: First DecisionRequest → Pipeline → MockExecutor → DecisionResult."""

import asyncio

from packages.decision_engine.contracts.models import DecisionRequest
from packages.decision_engine.domain.mock_executor import MockExecutor
from packages.decision_engine.pipeline.context import PipelineContext
from packages.decision_engine.registry.registry import StageRegistry


class MockIntentStage:
    async def process(self, context: PipelineContext) -> PipelineContext:
        return context


class MockExecutionStage:
    def __init__(self) -> None:
        self._executor = MockExecutor()

    async def process(self, context: PipelineContext) -> PipelineContext:
        tasks = [
            self._executor.execute(model, context.request.prompt)
            for model in context.request.models
        ]
        responses = await asyncio.gather(*tasks)
        return context.with_raw_responses(list(responses))


class MockNormalizationStage:
    async def process(self, context: PipelineContext) -> PipelineContext:
        normalized = []
        for resp in context.raw_responses:
            from packages.decision_engine.contracts.models import NormalizedResponse

            normalized.append(
                NormalizedResponse(
                    model=resp.model,
                    answer=resp.raw_response,
                    latency=resp.latency,
                    cost=resp.cost,
                    tokens=resp.tokens,
                )
            )
        return context.with_normalized_responses(normalized)


class MockDecisionStage:
    async def process(self, context: PipelineContext) -> PipelineContext:
        from packages.decision_engine.contracts.models import (
            Decision,
            DecisionResult,
            DecisionStatus,
            Explanation,
        )

        best = max(
            context.normalized_responses,
            key=lambda r: len(r.answer),
            default=None,
        )

        result = DecisionResult(
            request_id=context.request.request_id,
            decision=Decision(
                status=DecisionStatus.completed,
                summary=best.answer if best else "No responses",
            ),
            explanation=Explanation(
                why_selected="Selected the longest response as best answer.",
                reasoning="Mock mode: no real analysis performed.",
            ),
        )
        result.metrics.models_used = [r.model for r in context.normalized_responses]
        return context.with_result(result)


async def main() -> None:
    registry = StageRegistry()
    registry.register("intent", MockIntentStage())
    registry.register("execution", MockExecutionStage())
    registry.register("normalization", MockNormalizationStage())
    registry.register("decision", MockDecisionStage())

    from packages.decision_engine.pipeline.pipeline import DecisionPipeline

    pipeline = DecisionPipeline(registry)

    request = DecisionRequest(
        prompt="What is the best way to hash passwords?",
        models=["gpt-4o-mini", "claude-haiku", "gemini-flash"],
    )

    result = await pipeline.execute(request)

    print("=" * 60)  # noqa: T201
    print("SHURAH - First Decision")  # noqa: T201
    print("=" * 60)  # noqa: T201
    print(f"Request ID: {result.request_id}")  # noqa: T201
    print(f"Status: {result.decision.status}")  # noqa: T201
    print(f"Summary: {result.decision.summary[:100]}...")  # noqa: T201
    print(f"Confidence: {result.confidence.overall}")  # noqa: T201
    print(f"Models used: {result.metrics.models_used}")  # noqa: T201
    print(f"Explanation: {result.explanation.why_selected}")  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
