import pytest

from packages.decision_engine.domain.mock_executor import MockExecutor


class TestMockExecutor:
    @pytest.mark.asyncio
    async def test_execute_returns_response(self) -> None:
        executor = MockExecutor()
        response = await executor.execute("gpt-4o-mini", "How to hash passwords?")
        assert response.model == "gpt-4o-mini"
        assert response.status.value == "success"
        assert len(response.raw_response) > 0

    @pytest.mark.asyncio
    async def test_execute_known_model(self) -> None:
        executor = MockExecutor()
        response = await executor.execute("claude-haiku", "test")
        assert "Argon2id" in response.raw_response

    @pytest.mark.asyncio
    async def test_execute_unknown_model(self) -> None:
        executor = MockExecutor()
        response = await executor.execute("unknown-model", "test")
        assert response.status.value == "success"
        assert "not available" in response.raw_response
