"""Models for the SABnzbd queue API."""

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.types import SerializationStrategy

from aiosabnzbd.const import QueueStatus


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


@dataclass(frozen=True, kw_only=True, slots=True)
class Slot:
    """Representation of a download slot in the queue."""

    status: QueueStatus
    index: int
    password: str
    avg_age: str
    script: str
    direct_unpack: str
    mb: str
    mb_left: str = field(metadata={"alias": "mbleft"})
    mb_missing: str = field(metadata={"alias": "mbmissing"})
    size: str
    size_left: str = field(metadata={"alias": "sizeleft"})
    filename: str
    labels: list[str]
    priority: str
    cat: str
    timeleft: str
    percentage: str
    nzo_id: str
    unpack_opts: str = field(metadata={"alias": "unpackopts"})


@dataclass(frozen=True, kw_only=True, slots=True)
class Queue(DataClassORJSONMixin):
    """Representation the queue."""

    class Config(BaseConfig):
        """Mashumaro configuration."""

        serialization_strategy = {float: SABnzbdFileSize()}  # noqa: RUF012
        serialize_by_alias = True
        omit_none = True

    status: QueueStatus
    speedlimit: str
    speedlimit_absolut: str = field(metadata={"alias": "speedlimit_abs"})
    paused: bool
    noofslots_total: int
    noofslots: int
    limit: int
    start: int
    timeleft: timedelta = field(
        metadata=field_options(
            serialization_strategy=HumanReadableAsTimeDelta(fmt="%H:%M:%S")
        )
    )
    speed: str
    kb_per_sec: str = field(metadata={"alias": "kbpersec"})
    size: float
    size_left: float = field(metadata={"alias": "sizeleft"})
    megabyte: str = field(metadata={"alias": "mb"})
    megabyte_left: str = field(metadata={"alias": "mbleft"})
    slots: list[Slot]
    diskspace1: float
    diskspace2: float
    diskspace_total1: float = field(metadata={"alias": "diskspacetotal1"})
    diskspace_total2: float = field(metadata={"alias": "diskspacetotal2"})
    diskspace1_norm: float
    diskspace2_norm: float
    have_warnings: str
    pause_int: str
    left_quota: float
    version: str
    finish: int
    cache_article: str = field(metadata={"alias": "cache_art"})
    cache_size: float
    finish_action: str = field(metadata={"alias": "finishaction"})
    paused_all: bool
    quota: float
    have_quota: bool


@dataclass(frozen=True, kw_only=True, slots=True)
class QueueResponse(DataClassORJSONMixin):
    """Queue API response."""

    queue: Queue
