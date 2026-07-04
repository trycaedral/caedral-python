from __future__ import annotations

from typing import Any

from caedral.http import HttpClient
from caedral.types import EmbeddingCreateResponse


class EmbeddingsResource:
    """Text embeddings endpoint (``POST /v1/embeddings``)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        *,
        model: str,
        input: str | list[str],
        **kwargs: Any,
    ) -> EmbeddingCreateResponse:
        """Generate dense vector embeddings for one or more inputs.

        Args:
            model: Embedding model identifier (for example
                ``"caedral-embed"``).
            input: A single string or a list of strings to embed.
                When a list is provided, the response returns one
                vector per input in the same order.
            **kwargs: Additional request fields forwarded to the API.

        Returns:
            An :class:`EmbeddingCreateResponse` containing the
            generated vectors and token usage.

        Raises:
            CaedralAPIError: If the API returns a non-2xx response.
        """
        body = {"model": model, "input": input, **kwargs}
        data = self._http.post_json("/v1/embeddings", body)
        return EmbeddingCreateResponse.model_validate(data)
