from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any, Callable, TypeVar

import httpx

from caedral.errors import CaedralAPIError

T = TypeVar("T")


def iter_sse_json(
    response: httpx.Response,
    *,
    model_factory: Callable[[dict[str, Any]], T],
) -> Iterator[T]:
    """Parse Server-Sent Events lines into JSON objects."""
    if response.is_closed:
        raise CaedralAPIError("Streaming response has no body", status_code=502)

    buffer = ""
    for chunk in response.iter_text():
        buffer += chunk
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            parsed = _parse_sse_line(line.strip(), model_factory)
            if parsed is not None:
                yield parsed

    trailing = buffer.strip()
    if trailing:
        parsed = _parse_sse_line(trailing, model_factory)
        if parsed is not None:
            yield parsed


def _parse_sse_line(
    line: str,
    model_factory: Callable[[dict[str, Any]], T],
) -> T | None:
    if not line.startswith("data:"):
        return None

    data = line[len("data:") :].strip()
    if not data or data == "[DONE]":
        return None

    try:
        payload = json.loads(data)
    except json.JSONDecodeError as exc:
        raise CaedralAPIError(
            "Failed to parse streaming response chunk",
            status_code=502,
            error_type="upstream_error",
        ) from exc

    if not isinstance(payload, dict):
        raise CaedralAPIError(
            "Invalid streaming chunk payload",
            status_code=502,
            error_type="upstream_error",
        )

    return model_factory(payload)
