from __future__ import annotations

import math

import pytest

from caedral.embeddings import (
    DEFAULT_EMBEDDING_DIMENSIONS,
    DEFAULT_EMBEDDING_MODEL,
    EmbeddingValidationError,
    validate_embedding_dimensions,
    validate_embedding_model,
)
from caedral.resources.embeddings import EmbeddingsResource


class _FakeHttp:
    def __init__(self) -> None:
        self.last_body: dict | None = None

    def post_json(self, path: str, body: dict) -> dict:
        self.last_body = body
        return {
            "object": "list",
            "model": DEFAULT_EMBEDDING_MODEL,
            "data": [
                {
                    "object": "embedding",
                    "index": 0,
                    "embedding": [0.1] * DEFAULT_EMBEDDING_DIMENSIONS,
                }
            ],
            "usage": {"prompt_tokens": 1, "total_tokens": 1, "completion_tokens": 0},
        }


def test_defaults() -> None:
    assert validate_embedding_model(DEFAULT_EMBEDDING_MODEL) == DEFAULT_EMBEDDING_MODEL
    assert validate_embedding_dimensions(384) == 384


def test_rejects_bge() -> None:
    with pytest.raises(EmbeddingValidationError):
        validate_embedding_model("BAAI/bge-m3")


def test_create_sends_384() -> None:
    http = _FakeHttp()
    resource = EmbeddingsResource(http)  # type: ignore[arg-type]
    response = resource.create(input="query: exemplo")
    assert http.last_body == {
        "model": DEFAULT_EMBEDDING_MODEL,
        "dimensions": 384,
        "input": "query: exemplo",
    }
    assert len(response.data[0].embedding) == 384
    assert all(math.isfinite(v) for v in response.data[0].embedding)
