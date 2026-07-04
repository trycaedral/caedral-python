from __future__ import annotations

from typing import Any

from caedral.http import HttpClient
from caedral.resources.audio import AudioResource
from caedral.resources.chat import ChatResource
from caedral.resources.embeddings import EmbeddingsResource
from caedral.resources.images import ImagesResource
from caedral.resources.models import ModelsResource
from caedral.resources.rerank import RerankResource
from caedral.resources.usage import UsageResource


class Caedral:
    """Official synchronous Python client for the Caedral API."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.caedral.com",
        max_retries: int = 3,
        timeout: float = 120.0,
        **_: Any,
    ) -> None:
        """Create a new Caedral client.

        Args:
            api_key: Caedral API key used to authenticate every request.
                Must be a non-empty, non-blank string.
            base_url: Base URL of the Caedral API gateway. Defaults to
                the production endpoint; use ``http://localhost:5001``
                for local development.
            max_retries: Maximum number of automatic retries for
                idempotent (GET) requests. Defaults to ``3``.
            timeout: Per-request timeout in seconds. Defaults to
                ``120.0``.

        Raises:
            ValueError: If ``api_key`` is missing or blank.
        """
        if not api_key or not api_key.strip():
            raise ValueError("Caedral: api_key is required")

        self._http = HttpClient(
            api_key=api_key.strip(),
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
        )

        self.chat = ChatResource(self._http)
        self.models = ModelsResource(self._http)
        self.usage = UsageResource(self._http)
        self.embeddings = EmbeddingsResource(self._http)
        self.images = ImagesResource(self._http)
        self.audio = AudioResource(self._http)
        self.rerank = RerankResource(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Caedral:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
