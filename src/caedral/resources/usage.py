from __future__ import annotations

from caedral.http import HttpClient
from caedral.types import UsageSummary


class UsageResource:
    """Account usage endpoint (``GET /v1/usage``)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self) -> UsageSummary:
        """Fetch a snapshot of the account's current billing state.

        Returns:
            A :class:`UsageSummary` with prepaid ``accountStatus``,
            ``balanceCents``, and ``balanceMilliCents``. Plan/pool
            fields are optional leftovers from older payloads.

        Raises:
            CaedralAPIError: If the API returns a non-2xx response.
        """
        data = self._http.get("/v1/usage")
        return UsageSummary.model_validate(data)
