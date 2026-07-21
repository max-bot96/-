"""FastAPI app for Shurah Decision Engine."""
# ruff: noqa: E501

from __future__ import annotations

import asyncio

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from packages.decision_engine.contracts.models import DecisionRequest, DecisionResult
from packages.decision_engine.domain.mock_executor import MockExecutor
from packages.decision_engine.pipeline.context import PipelineContext
from packages.decision_engine.pipeline.pipeline import DecisionPipeline
from packages.decision_engine.registry.registry import StageRegistry

app = FastAPI(title="Shurah", version="0.1.0")


class MockIntentStage:
    async def process(self, context: PipelineContext) -> PipelineContext:
        return context


class MockExecutionStage:
    def __init__(self) -> None:
        self._executor = MockExecutor()

    async def process(self, context: PipelineContext) -> PipelineContext:
        tasks = [
            self._executor.execute(model, context.request.prompt)
            for model in context.request.models
        ]
        responses = await asyncio.gather(*tasks)
        return context.with_raw_responses(list(responses))


class MockNormalizationStage:
    async def process(self, context: PipelineContext) -> PipelineContext:
        from packages.decision_engine.contracts.models import NormalizedResponse

        normalized = [
            NormalizedResponse(
                model=resp.model,
                answer=resp.raw_response,
                latency=resp.latency,
                cost=resp.cost,
                tokens=resp.tokens,
            )
            for resp in context.raw_responses
        ]
        return context.with_normalized_responses(normalized)


class MockDecisionStage:
    async def process(self, context: PipelineContext) -> PipelineContext:
        from packages.decision_engine.contracts.models import (
            Decision,
            DecisionStatus,
            Explanation,
        )

        best = max(
            context.normalized_responses,
            key=lambda r: len(r.answer),
            default=None,
        )
        result = DecisionResult(
            request_id=context.request.request_id,
            decision=Decision(
                status=DecisionStatus.completed,
                summary=best.answer if best else "No responses",
            ),
            explanation=Explanation(
                why_selected="Selected the longest response as best answer.",
                reasoning="Mock mode: no real analysis performed.",
            ),
        )
        result.metrics.models_used = [r.model for r in context.normalized_responses]
        return context.with_result(result)


registry = StageRegistry()
registry.register("intent", MockIntentStage())
registry.register("execution", MockExecutionStage())
registry.register("normalization", MockNormalizationStage())
registry.register("decision", MockDecisionStage())

pipeline = DecisionPipeline(registry)


class PromptRequest(BaseModel):
    prompt: str
    models: list[str] = ["gpt-4o-mini", "claude-haiku", "gemini-flash"]


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>الشورة — Shurah</title>
<style>
body{font-family:system-ui,sans-serif;max-width:800px;margin:40px auto;padding:0 20px;background:#0d1117;color:#c9d1d9;line-height:1.6}
h1{color:#58a6ff;text-align:center;font-size:2.5rem;margin-bottom:0}
.subtitle{text-align:center;color:#8b949e;margin-top:5px}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:20px;margin:20px 0}
.card h2{margin-top:0;color:#58a6ff}
input,button{width:100%;padding:12px;margin:8px 0;border:1px solid #30363d;border-radius:6px;font-size:16px;box-sizing:border-box}
input{background:#0d1117;color:#c9d1d9}
button{background:#238636;color:#fff;border:none;cursor:pointer;font-weight:bold}
button:hover{background:#2ea043}
pre{background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:15px;overflow-x:auto;white-space:pre-wrap;direction:ltr;text-align:left}
.tag{display:inline-block;background:#1f6feb;color:#fff;padding:3px 10px;border-radius:12px;font-size:12px;margin:2px}
</style>
</head>
<body>
<h1>الشورة</h1>
<p class="subtitle">منصة لاتخاذ القرار بالاعتماد على عدة نماذج ذكاء اصطناعي</p>
<div class="card">
<h2>جرب الآن</h2>
<textarea id="prompt" rows="3" placeholder="اكتب سؤالك هنا..."></textarea>
<button onclick="decide()">أرسل</button>
</div>
<div id="result" style="display:none" class="card">
<h2>النتيجة</h2>
<pre id="output"></pre>
</div>
<script>
async function decide(){
const prompt=document.getElementById('prompt').value;
if(!prompt)return;
document.getElementById('result').style.display='block';
document.getElementById('output').textContent='جاري المعالجة...';
try{
const res=await fetch('/decide',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt})});
const data=await res.json();
document.getElementById('output').textContent=JSON.stringify(data,null,2);
}catch(e){document.getElementById('output').textContent='خطأ: '+e.message}
}
</script>
</body>
</html>"""


@app.post("/decide", response_model=DecisionResult)
async def decide(request: PromptRequest) -> DecisionResult:
    decision_request = DecisionRequest(
        prompt=request.prompt,
        models=request.models,
    )
    return await pipeline.execute(decision_request)
