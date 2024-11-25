"""SABnzbd wrapper."""

from .const import QueueOperationCommand, QueueStatus
from .exceptions import (
    SABnzbdConnectionError,
    SABnzbdConnectionTimeoutError,
    SABnzbdError,
    SABnzbdInvalidAPIKeyError,
    SABnzbdMissingAPIKeyError,
)
from .models.queue import Queue, QueueResponse, Slot
from .models.status import StatusResponse
from .sabnzbd import SABnzbdClient

__all__ = [
    "SABnzbdClient",
    "SABnzbdError",
    "SABnzbdConnectionError",
    "SABnzbdConnectionTimeoutError",
    "SABnzbdInvalidAPIKeyError",
    "SABnzbdMissingAPIKeyError",
    "QueueOperationCommand",
    "QueueStatus",
    "Queue",
    "Slot",
    "QueueResponse",
    "StatusResponse",
]
