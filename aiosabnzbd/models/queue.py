from dataclasses import dataclass

from mashumaro.mixins.orjson import DataClassORJSONMixin

from ..const import QueueOperationCommand, QueueStatus
from .base import SabnzbdRequest


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
    mbleft: str
    mbmissing: str
    size: str
    sizeleft: str
    filename: str
    labels: list[str]
    priority: str
    cat: str
    timeleft: str
    percentage: str
    nzo_id: str
    unpackopts: str


@dataclass(frozen=True, kw_only=True, slots=True)
class Queue(DataClassORJSONMixin):
    """Representation the queue."""

    status: QueueStatus
    speedlimit: str
    speedlimit_abs: str
    paused: bool
    noofslots_total: int
    noofslots: int
    limit: int
    start: int
    timeleft: str
    speed: str
    kbpersec: str
    size: str
    sizeleft: str
    mb: str
    mbleft: str
    slots: list[Slot]
    diskspace1: str
    diskspace2: str
    diskspacetotal1: str
    diskspacetotal2: str
    diskspace1_norm: str
    diskspace2_norm: str
    have_warnings: str
    pause_int: str
    left_quota: str
    version: str
    finish: int
    cache_art: str
    cache_size: str
    finishaction: str
    paused_all: bool
    quota: str
    have_quota: bool


@dataclass(frozen=True, kw_only=True, slots=True)
class QueueResponse(DataClassORJSONMixin):
    """Queue API response."""

    queue: Queue


@dataclass(kw_only=True)
class QueueRequest(SabnzbdRequest):
    """Request to get the latest queue data."""

    @property
    def query_params(self) -> dict[str, str]:
        """Return the query parameters."""
        return {"mode": "queue"}


@dataclass(kw_only=True)
class QueueOperationRequest(SabnzbdRequest):
    """Request to perform a queue operation."""

    mode: QueueOperationCommand

    @property
    def query_params(self) -> dict[str, str]:
        """Return the query parameters."""
        return {"mode": self.mode}
