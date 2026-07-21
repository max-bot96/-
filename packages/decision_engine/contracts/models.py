from __future__ import annotations

from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskType(StrEnum):
    code_generation = "code_generation"
    explanation = "explanation"
    debugging = "debugging"
    translation = "translation"
    research = "research"
    writing = "writing"
    analysis = "analysis"
    unknown = "unknown"


class Complexity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class Priority(StrEnum):
    speed = "speed"
    quality = "quality"
    security = "security"
    cost = "cost"


class DecisionStatus(StrEnum):
    completed = "completed"
    partial = "partial"
    failed = "failed"


class ModelStatus(StrEnum):
    success = "success"
    timeout = "timeout"
    cancelled = "cancelled"
    max_tokens = "max_tokens"
    content_filter = "content_filter"
    error = "error"


class DecisionType(StrEnum):
    consensus = "consensus"
    best_evidence = "best_evidence"
    risk_aware = "risk_aware"
    comparative = "comparative"


class Intent(BaseModel):
    task_type: str = "unknown"
    domain: str = "general"
    language: str = "unknown"
    complexity: str = "medium"
    priority: str = "quality"


class SessionContext(BaseModel):
    id: str = ""
    goal: str = ""
    language: str = "ar"
    history_reference: str | None = None


class UserContext(BaseModel):
    experience_level: str = "intermediate"
    preferred_language: str = "ar"
    risk_tolerance: str = "medium"
    domain: str = "general"


class ProjectContext(BaseModel):
    name: str = ""
    type: str = ""
    stack: list[str] = []
    architecture: str = ""


class MemoryContext(BaseModel):
    facts: list[str] = []
    preferences: dict[str, str] = {}
    previous_decisions: list[str] = []


class Constraints(BaseModel):
    budget: float | None = None
    latency: float | None = None
    max_tokens: int | None = None
    required_models: list[str] = []
    forbidden_models: list[str] = []


class Metadata(BaseModel):
    timestamp: str = ""
    api_version: str = "1.0"
    client: str = ""
    region: str = ""
    trace_id: str = ""


class DecisionRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    session: dict[str, str] = {}
    user: dict[str, str] = {}
    project: dict[str, str] = {}
    prompt: str
    models: list[str] = []
    memory: dict[str, str] = {}
    attachments: list[str] = []
    constraints: dict[str, str] = {}
    metadata: dict[str, str] = {}


class ModelResponse(BaseModel):
    id: str = ""
    model: str = ""
    provider: str = ""
    version: str = ""
    status: ModelStatus = ModelStatus.success
    cost: float = 0.0
    latency: float = 0.0
    tokens: int = 0
    raw_response: str = ""
    finish_reason: str = ""


class NormalizedResponse(BaseModel):
    model: str = ""
    status: ModelStatus = ModelStatus.success
    finish_reason: str = ""
    answer: str = ""
    code_blocks: list[str] = []
    warnings: list[str] = []
    citations: list[str] = []
    language: str = "ar"
    latency: float = 0.0
    cost: float = 0.0
    tokens: int = 0


class Agreement(BaseModel):
    points: list[str] = []
    models: list[str] = []


class Conflict(BaseModel):
    point: str = ""
    models: dict[str, str] = {}
    severity: str = "medium"


class Evidence(BaseModel):
    claim: str = ""
    source: str = ""
    strength: float = 0.0


class Risk(BaseModel):
    description: str = ""
    severity: str = "low"
    mitigation: str = ""


class Alternative(BaseModel):
    description: str = ""
    reason_rejected: str = ""


class Analysis(BaseModel):
    agreements: list[Agreement] = []
    conflicts: list[Conflict] = []
    evidence: list[Evidence] = []
    risks: list[Risk] = []
    alternatives: list[Alternative] = []


class Recommendation(BaseModel):
    best_option: str = ""
    next_step: str = ""
    priority: str = "medium"


class Explanation(BaseModel):
    why_selected: str = ""
    why_rejected: str = ""
    reasoning: str = ""
    tradeoffs: str = ""


class Confidence(BaseModel):
    overall: float = 0.0
    by_category: dict[str, float] = {}
    uncertainty: str = ""


class DecisionMetrics(BaseModel):
    latency: float = 0.0
    cost: float = 0.0
    tokens: int = 0
    models_used: list[str] = []


class Audit(BaseModel):
    decision_version: str = "1.0"
    rules_applied: list[str] = []
    pipeline_version: str = "1.0"


class DecisionManifest(BaseModel):
    engine_version: str = "1.0.0"
    pipeline_stages_executed: list[str] = []
    models_participated: list[str] = []
    rules_applied: list[str] = []
    confidence_factors: list[str] = []
    decision_timestamp: str = ""
    explanation_available: bool = False


class Decision(BaseModel):
    status: DecisionStatus = DecisionStatus.completed
    type: DecisionType = DecisionType.best_evidence
    summary: str = ""
    final_answer: str = ""


class DecisionResult(BaseModel):
    request_id: str = ""
    decision: Decision = Field(default_factory=Decision)
    analysis: Analysis = Field(default_factory=Analysis)
    recommendation: Recommendation = Field(default_factory=Recommendation)
    explanation: Explanation = Field(default_factory=Explanation)
    confidence: Confidence = Field(default_factory=Confidence)
    metrics: DecisionMetrics = Field(default_factory=DecisionMetrics)
    manifest: DecisionManifest = Field(default_factory=DecisionManifest)
    metadata: dict[str, str] = {}
