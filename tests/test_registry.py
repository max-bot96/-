from packages.decision_engine.pipeline.context import PipelineContext
from packages.decision_engine.registry.registry import StageRegistry


class FakeStage:
    def __init__(self, name: str) -> None:
        self.name = name

    async def process(self, context: PipelineContext) -> PipelineContext:
        return context


class TestStageRegistry:
    def test_register_stage(self) -> None:
        registry = StageRegistry()
        stage = FakeStage("test")
        registry.register("test", stage)
        assert registry.get("test") is not None

    def test_ordered_stages(self) -> None:
        registry = StageRegistry()
        stage_a = FakeStage("a")
        stage_b = FakeStage("b")
        registry.register("a", stage_a)
        registry.register("b", stage_b)
        assert len(registry.ordered_stages) == 2

    def test_insert_after(self) -> None:
        registry = StageRegistry()
        a = FakeStage("a")
        b = FakeStage("b")
        c = FakeStage("c")
        registry.register("a", a)
        registry.register("b", b)
        registry.insert_after("a", "c", c)
        stages = registry.ordered_stages
        assert stages[0] == a
        assert stages[1] == c
        assert stages[2] == b

    def test_insert_before(self) -> None:
        registry = StageRegistry()
        a = FakeStage("a")
        b = FakeStage("b")
        c = FakeStage("c")
        registry.register("a", a)
        registry.register("b", b)
        registry.insert_before("b", "c", c)
        stages = registry.ordered_stages
        assert stages[0] == a
        assert stages[1] == c
        assert stages[2] == b

    def test_remove_stage(self) -> None:
        registry = StageRegistry()
        a = FakeStage("a")
        b = FakeStage("b")
        registry.register("a", a)
        registry.register("b", b)
        registry.remove("a")
        assert len(registry.ordered_stages) == 1

    def test_replace_stage(self) -> None:
        registry = StageRegistry()
        a = FakeStage("a")
        b = FakeStage("b")
        registry.register("a", a)
        registry.replace("a", b)
        assert registry.get("a") is b
