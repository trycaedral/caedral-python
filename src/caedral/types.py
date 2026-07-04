from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class CaedralBaseModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class ChatMessageParam(CaedralBaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str | None
    name: str | None = None


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


class UsageSummary(CaedralBaseModel):
    accountStatus: str
    plan: str
    planStatus: str
    balanceCents: int
    weeklyPool: WeeklyPool
    overage: OverageSummary
    balanceWeightedUnitsAffordable: int


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
