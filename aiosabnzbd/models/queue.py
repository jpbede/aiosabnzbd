"""Models for the SABnzbd queue API."""

from dataclasses import dataclass, field
from datetime import timedelta

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin

from aiosabnzbd.const import QueueStatus
from aiosabnzbd.strategies import HumanReadableAsTimeDelta, SABnzbdFileSize


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
    speedlimit: int
    speedlimit_absolut: float = field(metadata={"alias": "speedlimit_abs"})
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
    speed: float
    kb_per_sec: float = field(metadata={"alias": "kbpersec"})
    size: float
    size_left: float = field(metadata={"alias": "sizeleft"})
    megabyte: float = field(metadata={"alias": "mb"})
    megabyte_left: float = field(metadata={"alias": "mbleft"})
    slots: list[Slot]
    diskspace1: float
    diskspace2: float
    diskspace_total1: float = field(metadata={"alias": "diskspacetotal1"})
    diskspace_total2: float = field(metadata={"alias": "diskspacetotal2"})
    diskspace1_norm: float
    diskspace2_norm: float
    have_warnings: int
    pause_int: int
    left_quota: float
    version: str
    finish: int
    cache_article: int = field(metadata={"alias": "cache_art"})
    cache_size: float
    finish_action: str = field(metadata={"alias": "finishaction"})
    paused_all: bool
    quota: float
    have_quota: bool


@dataclass(frozen=True, kw_only=True, slots=True)
class QueueResponse(DataClassORJSONMixin):
    """Queue API response."""

    queue: Queue
