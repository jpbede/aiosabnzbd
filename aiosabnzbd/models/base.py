"""Base models for aiosabnzbd."""

from dataclasses import dataclass


@dataclass(kw_only=True)
class SABnzbdRequest:
    """Base request."""

    mode: str | None = None
    name: str | None = None
    value: str | int | None = None

    @property
    def query_params(self) -> dict[str, str]:
        """Return the query parameters."""
        params = {}
        if self.mode is not None:
            params["mode"] = self.mode
        if self.name is not None:
            params["name"] = self.name
        if self.value is not None:
            params["value"] = str(self.value)

        return params
