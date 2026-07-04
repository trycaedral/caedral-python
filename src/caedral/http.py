from __future__ import annotations

import json
import time
from typing import Any

import httpx

from caedral.errors import CaedralAPIError, CaedralNetworkError

DEFAULT_BASE_URL = "https://api.caedral.com"
DEFAULT_MAX_RETRIES = 3
DEFAULT_TIMEOUT = 120.0


class HttpClient:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float = DEFAULT_TIMEOUT,
        client: httpx.Client | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=timeout)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def get(self, path: str) -> Any:
        return self._request_with_retry("GET", path)

    def post_json(self, path: str, body: dict[str, Any]) -> Any:
        return self._request("POST", path, json_body=body)

    def post_stream(self, path: str, body: dict[str, Any]) -> httpx.Response:
        request = self._client.build_request(
            "POST",
            f"{self.base_url}{path}",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=body,
        )
        try:
            return self._client.send(request, stream=True)
        except httpx.TimeoutException as exc:
            raise CaedralNetworkError(
                f"Request timed out after {self.timeout}s",
                cause=exc,
            ) from exc
        except httpx.HTTPError as exc:
            raise CaedralNetworkError(str(exc) or "Network request failed", cause=exc) from exc

    def _request_with_retry(self, method: str, path: str) -> Any:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                return self._request(method, path)
            except Exception as exc:
                last_error = exc
                if not self._should_retry(exc, attempt):
                    raise
                time.sleep(self._backoff_ms(attempt) / 1000)
        assert last_error is not None
        raise last_error

    def _should_retry(self, err: Exception, attempt: int) -> bool:
        if attempt >= self.max_retries:
            return False
        if isinstance(err, CaedralNetworkError):
            return True
        if isinstance(err, CaedralAPIError):
            return err.status_code in (502, 503)
        return False

    @staticmethod
    def _backoff_ms(attempt: int) -> int:
        return 100 * (2**attempt)

    def _request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        response = self._request_raw(method, path, json_body=json_body)
        text = response.text
        parsed = _safe_json_parse(text) if text else None
        if response.status_code >= 400:
            raise CaedralAPIError.from_response(response.status_code, parsed or text)
        return parsed

    def _request_raw(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
    ) -> httpx.Response:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if json_body is not None:
            headers["Content-Type"] = "application/json"

        try:
            return self._client.request(
                method,
                f"{self.base_url}{path}",
                headers=headers,
                json=json_body,
                timeout=self.timeout,
            )
        except httpx.TimeoutException as exc:
            raise CaedralNetworkError(
                f"Request timed out after {self.timeout}s",
                cause=exc,
            ) from exc
        except httpx.HTTPError as exc:
            raise CaedralNetworkError(str(exc) or "Network request failed", cause=exc) from exc


def _safe_json_parse(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text
