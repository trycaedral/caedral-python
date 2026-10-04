from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class CaedralBaseModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class NotreOptions(CaedralBaseModel):
    mode: Literal["off", "auto"] | None = None
    telemetry: bool | None = None


class NotreSavedBreakdown(CaedralBaseModel):
    cache_hit_tokens: int | None = None
    dedup_tokens: int | None = None
    prefilter_tokens: int | None = None


class NotrePublicMetadata(CaedralBaseModel):
    enabled: bool
    mode: Literal["off", "auto", "shadow"]
    intervened: bool
    fallback_used: bool
    input_before: int | None = None
    input_sent: int | None = None
    input_saved: int | None = None
    value_usd: float | None = None
    result: Literal["optimized", "no_gain", "fallback"] | None = None
    # Contract V3 shape fields (embeddings/rerank economy).
    shape: Literal["chat", "embeddings", "rerank"] | None = None
    contract_version: int | None = None
    saved_breakdown: NotreSavedBreakdown | None = None


class ChatMessageParam(CaedralBaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str | None
    name: str | None = None


class ChatCompletionCreateParams(CaedralBaseModel):
    model: str
    messages: list[ChatMessageParam]
    stream: bool | None = None
    notre: NotreOptions | None = None


class ChatCompletionChoice(CaedralBaseModel):
    index: int
    message: dict[str, Any]
    finish_reason: str | None = None


class CompletionUsage(CaedralBaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatCompletion(CaedralBaseModel):
    id: str
    object: Literal["chat.completion"] = "chat.completion"
    created: int
    model: str
    choices: list[ChatCompletionChoice]
    usage: CompletionUsage | None = None
    notre: NotrePublicMetadata | None = None


class ChatCompletionChunkChoice(CaedralBaseModel):
    index: int
    delta: dict[str, Any] = Field(default_factory=dict)
    finish_reason: str | None = None


class ChatCompletionChunk(CaedralBaseModel):
    id: str
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int
    model: str
    choices: list[ChatCompletionChunkChoice]


class Model(CaedralBaseModel):
    id: str
    object: Literal["model"] = "model"
    created: int
    owned_by: str
    name: str
    description: str
    context_window: int
    pricing_tier: str


class ModelListResponse(CaedralBaseModel):
    object: Literal["list"] = "list"
    data: list[Model]


class WeeklyPool(CaedralBaseModel):
    limit: int
    used: int
    remaining: int


class OverageSummary(CaedralBaseModel):
    enabled: bool
    limitCents: int | None = None
    usedCents: int
    remainingCents: int | None = None


class UsagePool(CaedralBaseModel):
    usedMilli: int = 0
    limitMilli: int = 0
    usedFormatted: str | None = None
    limitFormatted: str | None = None
    percentUsed: float = 0
    available: bool = True


class UsagePlan(CaedralBaseModel):
    id: str
    name: str
    interval: str
    status: str
    priceCents: int | None = None


class UsageOnDemand(CaedralBaseModel):
    mode: str
    allowed: bool
    blocked: bool | None = None
    enabled: bool | None = None
    accruedMilli: int = 0
    spentMilli: int | None = None
    accruedFormatted: str | None = None
    spentFormatted: str | None = None


class UsageSummary(CaedralBaseModel):
    accountStatus: str
    plan: UsagePlan | None = None
    billingPeriod: dict[str, Any] | None = None
    pools: dict[str, UsagePool] | None = None
    onDemand: UsageOnDemand | None = None
    quota: dict[str, Any] | None = None


class EmbeddingData(CaedralBaseModel):
    object: str
    embedding: list[float]
    index: int


class EmbeddingCreateResponse(CaedralBaseModel):
    object: str
    model: str
    data: list[EmbeddingData]
    usage: CompletionUsage | None = None


class ImageData(CaedralBaseModel):
    url: str | None = None
    b64_json: str | None = None


class ImageGenerateResponse(CaedralBaseModel):
    model: str
    data: list[ImageData]
    usage: CompletionUsage | None = None


class AudioGenerateResponse(CaedralBaseModel):
    model: str
    choices: list[dict[str, Any]] | None = None
    usage: CompletionUsage | None = None


class RerankResult(CaedralBaseModel):
    index: int
    relevance_score: float


class RerankCreateResponse(CaedralBaseModel):
    model: str
    results: list[RerankResult]
