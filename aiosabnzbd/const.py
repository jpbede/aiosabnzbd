"""Constants for aiosabnzbd."""

from enum import StrEnum

API_BASE_URL = "https://api.electricitymap.org/v3"


class ApiEndpoints:
    """Class holding API endpoints."""

    CARBON_INTENSITY_HA = API_BASE_URL + "/home-assistant"
    ZONES = API_BASE_URL + "/zones"
    LATEST_CARBON_INTENSITY = API_BASE_URL + "/carbon-intensity/latest"
    HISTORY_CARBON_INTENSITY = API_BASE_URL + "/carbon-intensity/history"
    LATEST_POWER_BREAKDOWN = API_BASE_URL + "/power-breakdown/latest"
    HISTORY_POWER_BREAKDOWN = API_BASE_URL + "/power-breakdown/history"


class QueueStatus(StrEnum):
    """Enum for queue status."""

    IDLE = "Idle"
    QUEUED = "Queued"
    PAUSED = "Paused"
    DOWNLOADING = "Downloading"
    PROPAGATING = "Propagating"
    FETCHING = "Fetching"


class QueueOperationCommand(StrEnum):
    """Enum for queue operation command."""

    RESUME = "resume"
    PAUSE = "pause"
