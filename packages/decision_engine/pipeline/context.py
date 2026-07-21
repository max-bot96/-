from __future__ import annotations

from dataclasses import dataclass, field

from packages.decision_engine.contracts.models import (
    Decision,
    DecisionRequest,
    DecisionResult,
    Intent,
    ModelResponse,
    NormalizedResponse,
)


@dataclass
class PipelineContext:
    """Immutable pipeline context. Each stage returns a new instance."""

    request: DecisionRequest
    intent: Intent | None = None
    raw_responses: list[ModelResponse] = field(default_factory=list)
    normalized_responses: list[NormalizedResponse] = field(default_factory=list)
    decision: Decision | None = None
    result: DecisionResult | None = None
    errors: list[str] = field(default_factory=list)

    def with_intent(self, intent: Intent) -> PipelineContext:
        return PipelineContext(
            request=self.request,
            intent=intent,
            raw_responses=self.raw_responses,
            normalized_responses=self.normalized_responses,
            decision=self.decision,
            result=self.result,
            errors=self.errors,
        )

    def with_raw_responses(self, responses: list[ModelResponse]) -> PipelineContext:
        return PipelineContext(
            request=self.request,
            intent=self.intent,
            raw_responses=responses,
            normalized_responses=self.normalized_responses,
            decision=self.decision,
            result=self.result,
            errors=self.errors,
        )

    def with_normalized_responses(
        self, responses: list[NormalizedResponse]
    ) -> PipelineContext:
        return PipelineContext(
            request=self.request,
            intent=self.intent,
            raw_responses=self.raw_responses,
            normalized_responses=responses,
            decision=self.decision,
            result=self.result,
            errors=self.errors,
        )

    def with_decision(self, decision: Decision) -> PipelineContext:
        return PipelineContext(
            request=self.request,
            intent=self.intent,
            raw_responses=self.raw_responses,
            normalized_responses=self.normalized_responses,
            decision=decision,
            result=self.result,
            errors=self.errors,
        )

    def with_result(self, result: DecisionResult) -> PipelineContext:
        return PipelineContext(
            request=self.request,
            intent=self.intent,
            raw_responses=self.raw_responses,
            normalized_responses=self.normalized_responses,
            decision=self.decision,
            result=result,
            errors=self.errors,
        )

    def with_error(self, error: str) -> PipelineContext:
        return PipelineContext(
            request=self.request,
            intent=self.intent,
            raw_responses=self.raw_responses,
            normalized_responses=self.normalized_responses,
            decision=self.decision,
            result=self.result,
            errors=self.errors + [error],
        )
