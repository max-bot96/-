from __future__ import annotations

from packages.decision_engine.contracts.models import ModelResponse, ModelStatus


class MockExecutor:
    """Mock executor for testing without external API calls."""

    MOCK_RESPONSES: dict[str, str] = {
        "gpt-4o-mini": "Use bcrypt for password hashing.",
        "claude-haiku": "I recommend Argon2id for password hashing.",
        "gemini-flash": "For password hashing, use bcrypt or Argon2.",
    }

    async def execute(self, model: str, prompt: str) -> ModelResponse:  # noqa: ARG002
        response = self.MOCK_RESPONSES.get(model, "Mock response not available.")
        return ModelResponse(
            id=f"mock-{model}",
            model=model,
            provider="mock",
            version="1.0",
            status=ModelStatus.success,
            cost=0.001,
            latency=0.5,
            tokens=len(response.split()),
            raw_response=response,
            finish_reason="completed",
        )
