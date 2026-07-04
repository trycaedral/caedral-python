from __future__ import annotations

from caedral.http import HttpClient
from caedral.types import ModelListResponse


class ModelsResource:
    """Model catalog endpoint (``GET /v1/models``)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> ModelListResponse:
        """List every model available to the authenticated account.

        Returns:
            A :class:`ModelListResponse` describing each model along
            with its context window and pricing tier.

        Raises:
            CaedralAPIError: If the API returns a non-2xx response.
        """
        data = self._http.get("/v1/models")
        return ModelListResponse.model_validate(data)
