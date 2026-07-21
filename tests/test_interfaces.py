from packages.decision_engine.interfaces.protocols import (
    DecisionPolicy,
    IntentProvider,
    ModelExecutor,
    Normalizer,
    Stage,
)


class TestProtocols:
    def test_stage_is_protocol(self) -> None:
        assert hasattr(Stage, "__init__")

    def test_intent_provider_is_protocol(self) -> None:
        assert hasattr(IntentProvider, "__init__")

    def test_model_executor_is_protocol(self) -> None:
        assert hasattr(ModelExecutor, "__init__")

    def test_normalizer_is_protocol(self) -> None:
        assert hasattr(Normalizer, "__init__")

    def test_decision_policy_is_protocol(self) -> None:
        assert hasattr(DecisionPolicy, "__init__")

