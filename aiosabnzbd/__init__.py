"""SABnzbd wrapper."""

from .const import QueueOperationCommand, QueueStatus
from .exceptions import (
    SABnzbdConnectionError,
    SABnzbdConnectionTimeoutError,
    SABnzbdError,
    SABnzbdInvalidAPIKeyError,
    SABnzbdMissingAPIKeyError,
)
from .models import History, HistoryResponse
from .models.queue import Queue, QueueResponse, Slot
from .models.status import StatusResponse
from .sabnzbd import SABnzbdClient

__all__ = [
    "History",
    "HistoryResponse",
    "Queue",
    "QueueOperationCommand",
    "QueueResponse",
    "QueueStatus",
    "SABnzbdClient",
    "SABnzbdConnectionError",
    "SABnzbdConnectionTimeoutError",
    "SABnzbdError",
    "SABnzbdInvalidAPIKeyError",
    "SABnzbdMissingAPIKeyError",
    "Slot",
    "StatusResponse",
]
