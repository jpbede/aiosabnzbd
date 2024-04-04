from dataclasses import dataclass


@dataclass(kw_only=True)
class SabnzbdRequest:
    @property
    def query_params(self) -> dict[str, str]:
        """Return the query parameters."""
        return {}
