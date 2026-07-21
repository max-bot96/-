"""FastAPI app for Shurah Decision Engine."""

from __future__ import annotations

import asyncio

from fastapi import FastAPI
from pydantic import BaseModel

from packages.decision_engine.contracts.models import DecisionRequest, DecisionResult
from packages.decision_engine.domain.mock_executor import MockExecutor
from packages.decision_engine.pipeline.context import PipelineContext
from packages.decision_engine.pipeline.pipeline import DecisionPipeline
from packages.decision_engine.registry.registry import StageRegistry

app = FastAPI(title="Shurah", version="0.1.0")


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
        from packages.decision_engine.contracts.models import NormalizedResponse

        normalized = [
            NormalizedResponse(
                model=resp.model,
                answer=resp.raw_response,
                latency=resp.latency,
                cost=resp.cost,
                tokens=resp.tokens,
            )
            for resp in context.raw_responses
        ]
        return context.with_normalized_responses(normalized)


class MockDecisionStage:
    async def process(self, context: PipelineContext) -> PipelineContext:
        from packages.decision_engine.contracts.models import (
            Decision,
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


registry = StageRegistry()
registry.register("intent", MockIntentStage())
registry.register("execution", MockExecutionStage())
registry.register("normalization", MockNormalizationStage())
registry.register("decision", MockDecisionStage())

pipeline = DecisionPipeline(registry)


class PromptRequest(BaseModel):
    prompt: str
    models: list[str] = ["gpt-4o-mini", "claude-haiku", "gemini-flash"]


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Shurah Decision Engine", "version": "0.1.0"}


@app.post("/decide", response_model=DecisionResult)
async def decide(request: PromptRequest) -> DecisionResult:
    decision_request = DecisionRequest(
        prompt=request.prompt,
        models=request.models,
    )
    return await pipeline.execute(decision_request)
