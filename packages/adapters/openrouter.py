from __future__ import annotations

from typing import Any

from packages.decision_engine.contracts.models import ModelResponse, ModelStatus


def _calculate_cost(model: str, usage: dict[str, Any]) -> float:
    rates: dict[str, tuple[float, float]] = {
        "gpt-4o-mini": (0.15, 0.60),
        "gpt-4o": (2.50, 10.00),
        "claude-3.5-sonnet": (3.00, 15.00),
        "claude-3-haiku": (0.25, 1.25),
        "gemini-1.5-flash": (0.075, 0.30),
        "gemini-1.5-pro": (1.25, 5.00),
    }
    rate = rates.get(model, (1.00, 3.00))
    input_tokens = usage.get("prompt_tokens", 0) / 1000
    output_tokens = usage.get("completion_tokens", 0) / 1000
    result = (input_tokens * rate[0] + output_tokens * rate[1]) / 1000
    return round(float(result), 6)


class OpenRouterExecutor:
    """Executes prompts against models via OpenRouter API."""

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str, timeout: int = 30) -> None:
        self._api_key = api_key
        self._timeout = timeout

    async def execute(self, model: str, prompt: str) -> ModelResponse:
        import aiohttp

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://shurah.dev",
        }
        payload: dict[str, Any] = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            session = aiohttp.ClientSession()
            try:
                resp = await session.post(
                    self.BASE_URL,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self._timeout),
                )
                if resp.status != 200:
                    error_body = await resp.text()
                    return ModelResponse(
                        model=model,
                        provider="openrouter",
                        status=ModelStatus.error,
                        raw_response=f"HTTP {resp.status}: {error_body}",
                        finish_reason="error",
                    )

                data = await resp.json()
                choice = data.get("choices", [{}])[0]
                message = choice.get("message", {})
                content = message.get("content", "")

                usage = data.get("usage", {})
                cost = _calculate_cost(model, usage)

                return ModelResponse(
                    id=data.get("id", ""),
                    model=model,
                    provider="openrouter",
                    version=data.get("model", ""),
                    status=ModelStatus.success,
                    cost=cost,
                    latency=0.0,
                    tokens=usage.get("total_tokens", 0),
                    raw_response=content,
                    finish_reason=choice.get("finish_reason", "completed"),
                )
            finally:
                await session.close()
        except TimeoutError:
            return ModelResponse(
                model=model,
                provider="openrouter",
                status=ModelStatus.timeout,
                raw_response="Request timed out",
                finish_reason="timeout",
            )
        except Exception as e:
            return ModelResponse(
                model=model,
                provider="openrouter",
                status=ModelStatus.error,
                raw_response=str(e),
                finish_reason="error",
            )
