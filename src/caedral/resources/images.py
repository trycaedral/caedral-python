from __future__ import annotations

from typing import Any

from caedral.http import HttpClient
from caedral.types import ImageGenerateResponse


class ImagesResource:
    """Image generation endpoint (``POST /v1/images/generations``)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def generate(
        self,
        *,
        prompt: str,
        model: str | None = None,
        **kwargs: Any,
    ) -> ImageGenerateResponse:
        """Generate one or more images from a text prompt.

        Args:
            prompt: Natural-language description of the desired image.
            model: Optional model identifier. When omitted, the API
                selects a default image model.
            **kwargs: Additional request fields such as ``n`` (number
                of images) or ``size`` (output resolution).

        Returns:
            An :class:`ImageGenerateResponse` containing the generated
            images as URLs or base64-encoded data.

        Raises:
            CaedralAPIError: If the API returns a non-2xx response.
        """
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        data = self._http.post_json("/v1/images/generations", body)
        return ImageGenerateResponse.model_validate(data)
