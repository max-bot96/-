from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.decision_engine.contracts.models import (
    Decision,
    DecisionRequest,
    DecisionResult,
    Intent,
    ModelResponse,
    NormalizedResponse,
)
from packages.decision_engine.pipeline.context import PipelineContext


@runtime_checkable
class Stage(Protocol):
    """Base interface for all pipeline stages."""

    async def process(self, context: PipelineContext) -> PipelineContext:
        ...


@runtime_checkable
class IntentProvider(Protocol):
    """Analyzes user intent from the prompt."""

    async def analyze(self, prompt: str) -> Intent:
        ...


@runtime_checkable
class ModelExecutor(Protocol):
    """Executes a prompt against a single model."""

    async def execute(self, model: str, prompt: str) -> ModelResponse:
        ...


@runtime_checkable
class Normalizer(Protocol):
    """Normalizes raw model responses into a standard format."""

    async def normalize(self, response: ModelResponse) -> NormalizedResponse:
        ...


@runtime_checkable
class DecisionPolicy(Protocol):
    """Makes the final decision from normalized responses."""

    async def decide(
        self,
        responses: list[NormalizedResponse],
        context: PipelineContext,
    ) -> Decision:
        ...


@runtime_checkable
class Pipeline(Protocol):
    """Orchestrates the decision pipeline stages."""

    async def execute(self, request: DecisionRequest) -> DecisionResult:
        ...
