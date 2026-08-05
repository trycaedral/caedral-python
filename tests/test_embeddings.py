from __future__ import annotations

import math

import pytest

from caedral.embeddings import (
    CANONICAL_EMBEDDING_MODEL,
    DEFAULT_EMBEDDING_DIMENSIONS,
    DEFAULT_EMBEDDING_MODEL,
    LEGACY_EMBEDDING_MODEL,
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
            "model": CANONICAL_EMBEDDING_MODEL,
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
    assert DEFAULT_EMBEDDING_MODEL == CANONICAL_EMBEDDING_MODEL
    assert validate_embedding_model(CANONICAL_EMBEDDING_MODEL) == CANONICAL_EMBEDDING_MODEL
    assert validate_embedding_dimensions(384) == 384


def test_legacy_alias_maps_to_canonical() -> None:
    assert validate_embedding_model(LEGACY_EMBEDDING_MODEL) == CANONICAL_EMBEDDING_MODEL


def test_rejects_unsupported_model() -> None:
    with pytest.raises(EmbeddingValidationError):
        validate_embedding_model("BAAI/bge-m3")


def test_rejects_invalid_dimensions() -> None:
    with pytest.raises(EmbeddingValidationError):
        validate_embedding_dimensions(768)


def test_create_sends_defaults() -> None:
    http = _FakeHttp()
    resource = EmbeddingsResource(http)  # type: ignore[arg-type]
    response = resource.create(input="query: exemplo")
    assert http.last_body == {
        "model": CANONICAL_EMBEDDING_MODEL,
        "dimensions": 384,
        "input": "query: exemplo",
        "encoding_format": "float",
    }
    assert len(response.data[0].embedding) == 384
    assert all(math.isfinite(v) for v in response.data[0].embedding)


def test_create_with_legacy_alias() -> None:
    http = _FakeHttp()
    resource = EmbeddingsResource(http)  # type: ignore[arg-type]
    resource.create(input="hello", model=LEGACY_EMBEDDING_MODEL)
    assert http.last_body is not None
    assert http.last_body["model"] == CANONICAL_EMBEDDING_MODEL


def test_create_with_input_type_query() -> None:
    http = _FakeHttp()
    resource = EmbeddingsResource(http)  # type: ignore[arg-type]
    resource.create(input="search text", input_type="query")
    assert http.last_body == {
        "model": CANONICAL_EMBEDDING_MODEL,
        "dimensions": 384,
        "input": "search text",
        "encoding_format": "float",
        "input_type": "query",
    }


def test_create_with_input_type_document() -> None:
    http = _FakeHttp()
    resource = EmbeddingsResource(http)  # type: ignore[arg-type]
    resource.create(input="doc text", input_type="document")
    assert http.last_body == {
        "model": CANONICAL_EMBEDDING_MODEL,
        "dimensions": 384,
        "input": "doc text",
        "encoding_format": "float",
        "input_type": "document",
    }


def test_create_with_encoding_format_float() -> None:
    http = _FakeHttp()
    resource = EmbeddingsResource(http)  # type: ignore[arg-type]
    resource.create(input="text", encoding_format="float")
    assert http.last_body is not None
    assert http.last_body["encoding_format"] == "float"


def test_create_with_encoding_format_base64() -> None:
    http = _FakeHttp()
    resource = EmbeddingsResource(http)  # type: ignore[arg-type]
    resource.create(input="text", encoding_format="base64")
    assert http.last_body is not None
    assert http.last_body["encoding_format"] == "base64"
