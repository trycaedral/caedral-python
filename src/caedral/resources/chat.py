from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Literal, overload

from caedral._sse import iter_sse_json
from caedral.errors import CaedralAPIError
from caedral.http import HttpClient
from caedral.types import ChatCompletion, ChatCompletionChunk


class ChatCompletions:
    """Chat completions endpoint (``POST /v1/chat/completions``).

    Supports both buffered and Server-Sent Events (SSE) streaming
    responses; the return type of :meth:`create` depends on the
    ``stream`` flag.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    @overload
    def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: Literal[False] = False,
        **kwargs: Any,
    ) -> ChatCompletion: ...

    @overload
    def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: Literal[True],
        **kwargs: Any,
    ) -> Iterator[ChatCompletionChunk]: ...

    def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> ChatCompletion | Iterator[ChatCompletionChunk]:
        """Create a chat completion.

        Args:
            model: Model identifier (for example ``"caedral-base"``).
            messages: Ordered list of chat messages in OpenAI-style
                ``{"role": ..., "content": ...}`` format.
            stream: When ``False`` (default), the full completion is
                returned once ready. When ``True``, an iterator of
                incremental ``ChatCompletionChunk`` deltas is returned
                (SSE).
            **kwargs: Additional request fields (``temperature``,
                ``max_tokens``, ``top_p``, ``stop``, ``user``, etc.)
                forwarded to the API.

        Returns:
            A :class:`ChatCompletion` when not streaming, or an
            :class:`Iterator` of :class:`ChatCompletionChunk` when
            ``stream=True``.

        Raises:
            CaedralAPIError: If the API returns a non-2xx response.

        Example:
            Streaming::

                stream = client.chat.completions.create(
                    model="caedral-base",
                    messages=[{"role": "user", "content": "Hi"}],
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        print(delta, end="", flush=True)
        """
        body: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs,
        }

        if stream:
            return self._create_stream(body)
        data = self._http.post_json("/v1/chat/completions", body)
        return ChatCompletion.model_validate(data)

    def _create_stream(self, body: dict[str, Any]) -> Iterator[ChatCompletionChunk]:
        response = self._http.post_stream("/v1/chat/completions", body)
        try:
            if response.status_code >= 400:
                error_body: Any
                try:
                    error_body = response.json()
                except Exception:
                    error_body = response.read().decode("utf-8", errors="replace")
                raise CaedralAPIError.from_response(response.status_code, error_body)

            yield from iter_sse_json(
                response,
                model_factory=ChatCompletionChunk.model_validate,
            )
        finally:
            response.close()


class ChatResource:
    """Namespace grouping chat-related endpoints.

    Currently exposes :attr:`completions` for
    ``POST /v1/chat/completions``.
    """

    def __init__(self, http: HttpClient) -> None:
        self.completions = ChatCompletions(http)
