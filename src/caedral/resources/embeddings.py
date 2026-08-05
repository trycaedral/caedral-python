from __future__ import annotations

from typing import Any, Literal

from caedral.embeddings import (
    DEFAULT_EMBEDDING_DIMENSIONS,
    DEFAULT_EMBEDDING_MODEL,
    validate_embedding_dimensions,
    validate_embedding_model,
)
from caedral.http import HttpClient
from caedral.types import EmbeddingCreateResponse


class EmbeddingsResource:
    """Text embeddings endpoint (``POST /v1/embeddings``)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        *,
        input: str | list[str],
        model: str = DEFAULT_EMBEDDING_MODEL,
        dimensions: int = DEFAULT_EMBEDDING_DIMENSIONS,
        input_type: Literal["query", "document"] | None = None,
        encoding_format: Literal["float", "base64"] = "float",
        **kwargs: Any,
    ) -> EmbeddingCreateResponse:
        """Generate dense vector embeddings for one or more inputs."""
        model = validate_embedding_model(model)
        dimensions = validate_embedding_dimensions(dimensions)
        body: dict[str, Any] = {
            "model": model,
            "dimensions": dimensions,
            "input": input,
            "encoding_format": encoding_format,
            **kwargs,
        }
        if input_type is not None:
            body["input_type"] = input_type
        data = self._http.post_json("/v1/embeddings", body)
        return EmbeddingCreateResponse.model_validate(data)
