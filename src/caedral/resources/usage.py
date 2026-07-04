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
            A :class:`UsageSummary` describing the current plan,
            weekly free pool utilization, prepaid balance, and
            overage limits.

        Raises:
            CaedralAPIError: If the API returns a non-2xx response.
        """
        data = self._http.get("/v1/usage")
        return UsageSummary.model_validate(data)
