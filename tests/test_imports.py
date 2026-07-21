"""Sprint 0.1: Verify project structure imports correctly."""


def test_packages_importable() -> None:
    import packages  # noqa: F401
    import packages.adapters  # noqa: F401
    import packages.decision_engine  # noqa: F401
    import packages.decision_engine.contracts  # noqa: F401
    import packages.decision_engine.domain  # noqa: F401
    import packages.decision_engine.exceptions  # noqa: F401
    import packages.decision_engine.interfaces  # noqa: F401
    import packages.decision_engine.pipeline  # noqa: F401
    import packages.decision_engine.registry  # noqa: F401
    import packages.decision_engine.telemetry  # noqa: F401
    import packages.shared  # noqa: F401
