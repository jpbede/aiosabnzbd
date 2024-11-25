"""Mashumaro strategies."""

from datetime import UTC, datetime, timedelta

from mashumaro.types import SerializationStrategy


class HumanReadableAsTimeDelta(SerializationStrategy):
    """Serialization strategy for timedelta to humanreadable string."""

    def __init__(self, fmt: str) -> None:
        """Initialize the serialization strategy."""
        self.fmt = fmt

    def serialize(self, value: timedelta) -> str:
        """Serialize a timedelta to a humanreadable string."""
        d = datetime.now(tz=UTC) + value
        return d.strftime(self.fmt)

    def deserialize(self, value: str) -> timedelta:
        """Deserialize a humanreadable string to a timedelta."""
        d = datetime.strptime(value, self.fmt)  # noqa: DTZ007
        return timedelta(hours=d.hour, minutes=d.minute, seconds=d.second)


class SABnzbdFileSize(SerializationStrategy):
    """Serialization strategy for filesize to humanreadable string."""

    def serialize(self, value: float) -> str:
        """Serialize a filesize to a humanreadable string."""
        if value < 1.0:
            return "0 B"
        if value < 1024.0:
            return f"{value:.2f} B"
        if value < 1024.0 * 1024.0:
            return f"{value / 1024.0:.2f} K"
        if value < 1024.0 * 1024.0 * 1024.0:
            return f"{value / (1024.0 * 1024.0):.2f} M"

        return f"{value / (1024.0 * 1024.0 * 1024.0):.2f} T"

    def deserialize(self, value: str) -> float:
        """Deserialize a humanreadable string to a filesize."""
        suffix = value[-1]
        if suffix == "K":
            multiplier = 1.0 / (1024.0 * 1024.0)
        elif suffix == "M":
            multiplier = 1.0 / 1024.0
        elif suffix == "T":
            multiplier = 1024.0
        else:
            multiplier = 1

        try:
            val = float(value.split(" ")[0])
            return val * multiplier
        except ValueError:
            return 0.0
