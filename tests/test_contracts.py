from packages.decision_engine.contracts.models import (
    Decision,
    DecisionRequest,
    DecisionResult,
    DecisionStatus,
    ModelResponse,
    ModelStatus,
    NormalizedResponse,
)


class TestDecisionRequest:
    def test_minimal_request(self) -> None:
        req = DecisionRequest(prompt="Hello")
        assert req.prompt == "Hello"
        assert req.models == []

    def test_request_with_models(self) -> None:
        req = DecisionRequest(
            prompt="Write code",
            models=["gpt-4", "claude-3"],
        )
        assert len(req.models) == 2

    def test_request_id_is_unique(self) -> None:
        req1 = DecisionRequest(prompt="test")
        req2 = DecisionRequest(prompt="test")
        assert req1.request_id != req2.request_id


class TestDecisionResult:
    def test_minimal_result(self) -> None:
        result = DecisionResult(request_id="test-1")
        assert result.request_id == "test-1"
        assert result.decision.status == DecisionStatus.completed

    def test_with_decision(self) -> None:
        result = DecisionResult(
            request_id="test-2",
            decision=Decision(
                status=DecisionStatus.completed,
                summary="Best solution is Argon2id",
            ),
        )
        assert result.decision.summary == "Best solution is Argon2id"

    def test_manifest_present(self) -> None:
        result = DecisionResult(request_id="test-3")
        assert result.manifest.engine_version == "1.0.0"
        assert result.manifest.explanation_available is False

    def test_confidence_defaults(self) -> None:
        result = DecisionResult(request_id="test-4")
        assert result.confidence.overall == 0.0
        assert result.confidence.uncertainty == ""

    def test_metrics_defaults(self) -> None:
        result = DecisionResult(request_id="test-5")
        assert result.metrics.latency == 0.0
        assert result.metrics.cost == 0.0
        assert result.metrics.models_used == []


class TestModelResponse:
    def test_minimal(self) -> None:
        resp = ModelResponse(model="gpt-4")
        assert resp.model == "gpt-4"
        assert resp.status == ModelStatus.success

    def test_error_status(self) -> None:
        resp = ModelResponse(model="claude", status=ModelStatus.error)
        assert resp.status == ModelStatus.error


class TestNormalizedResponse:
    def test_minimal(self) -> None:
        resp = NormalizedResponse(model="gemini")
        assert resp.model == "gemini"
        assert resp.status == ModelStatus.success

    def test_with_code(self) -> None:
        resp = NormalizedResponse(
            model="gpt-4",
            answer="Use bcrypt",
            code_blocks=["import bcrypt"],
        )
        assert len(resp.code_blocks) == 1
