from __future__ import annotations

from typing import Any


class CaedralAPIError(Exception):
    """Raised when the Caedral API returns an error response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 0,
        error_type: str = "unknown",
        raw_body: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.type = error_type
        self.raw_body = raw_body

    @classmethod
    def from_response(cls, status_code: int, body: Any) -> CaedralAPIError:
        if isinstance(body, dict) and isinstance(body.get("error"), dict):
            error = body["error"]
            message = error.get("message") or f"Request failed with status {status_code}"
            return cls(
                message,
                status_code=error.get("code") or status_code,
                error_type=error.get("type") or "unknown",
                raw_body=body,
            )

        if isinstance(body, dict) and isinstance(body.get("message"), str):
            return cls(body["message"], status_code=status_code, raw_body=body)

        if isinstance(body, str) and body.strip():
            return cls(body, status_code=status_code, raw_body=body)

        return cls(
            f"Request failed with status {status_code}",
            status_code=status_code,
            raw_body=body,
        )

    def __repr__(self) -> str:
        return (
            f"CaedralAPIError(message={self.message!r}, "
            f"status_code={self.status_code}, type={self.type!r})"
        )


class CaedralNetworkError(CaedralAPIError):
    """Raised on network failures or timeouts."""

    def __init__(self, message: str, *, cause: BaseException | None = None) -> None:
        super().__init__(message, status_code=0, error_type="network_error")
        self.__cause__ = cause
