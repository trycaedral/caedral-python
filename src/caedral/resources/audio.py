from __future__ import annotations

from typing import Any

from caedral.http import HttpClient
from caedral.types import AudioGenerateResponse


class AudioResource:
    """Audio (text-to-speech) endpoint (``POST /v1/audio/speech``)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def generate(
        self,
        *,
        input: str,
        model: str | None = None,
        voice: str | None = None,
        **kwargs: Any,
    ) -> AudioGenerateResponse:
        """Synthesize speech audio from an input text string.

        Args:
            input: Text to convert to speech.
            model: Optional model identifier. When omitted, the API
                selects a default speech model.
            voice: Optional voice identifier or style hint.
            **kwargs: Additional request fields forwarded to the API.

        Returns:
            An :class:`AudioGenerateResponse` containing the generated
            audio payload.

        Raises:
            CaedralAPIError: If the API returns a non-2xx response.
        """
        body: dict[str, Any] = {"input": input, **kwargs}
        if model is not None:
            body["model"] = model
        if voice is not None:
            body["voice"] = voice
        data = self._http.post_json("/v1/audio/speech", body)
        return AudioGenerateResponse.model_validate(data)
