"""Models for the SABnzbd queue API."""

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from mashumaro import field_options
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
    size: str
    size_left: str = field(metadata={"alias": "sizeleft"})
    megabyte: str = field(metadata={"alias": "mb"})
    megabyte_left: str = field(metadata={"alias": "mbleft"})
    slots: list[Slot]
    diskspace1: str
    diskspace2: str
    diskspace_total1: str = field(metadata={"alias": "diskspacetotal1"})
    diskspace_total2: str = field(metadata={"alias": "diskspacetotal2"})
    diskspace1_norm: str
    diskspace2_norm: str
    have_warnings: str
    pause_int: str
    left_quota: str
    version: str
    finish: int
    cache_article: str = field(metadata={"alias": "cache_art"})
    cache_size: str
    finish_action: str = field(metadata={"alias": "finishaction"})
    paused_all: bool
    quota: str
    have_quota: bool


@dataclass(frozen=True, kw_only=True, slots=True)
class QueueResponse(DataClassORJSONMixin):
    """Queue API response."""

    queue: Queue
