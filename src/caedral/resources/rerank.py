from __future__ import annotations

from typing import Any

from caedral.http import HttpClient
from caedral.types import RerankCreateResponse


class RerankResource:
    """Document rerank endpoint (``POST /v1/rerank``)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        *,
        query: str,
        documents: list[str],
        model: str | None = None,
        top_n: int | None = None,
        **kwargs: Any,
    ) -> RerankCreateResponse:
        """Reorder documents by semantic relevance to a query.

        Args:
            query: Query text used to score the documents.
            documents: List of candidate documents to rerank.
            model: Optional model identifier. When omitted, the API
                selects a default rerank model.
            top_n: Optional cap on the number of results returned,
                keeping only the top-N most relevant documents.
            **kwargs: Additional request fields forwarded to the API.

        Returns:
            A :class:`RerankCreateResponse` with relevance-scored
            results ordered from most to least relevant.

        Raises:
            CaedralAPIError: If the API returns a non-2xx response.
        """
        body: dict[str, Any] = {
            "query": query,
            "documents": documents,
            **kwargs,
        }
        if model is not None:
            body["model"] = model
        if top_n is not None:
            body["top_n"] = top_n
        data = self._http.post_json("/v1/rerank", body)
        return RerankCreateResponse.model_validate(data)
