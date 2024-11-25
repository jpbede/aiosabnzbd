"""History models."""

from dataclasses import dataclass

from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin

from aiosabnzbd.strategies import SABnzbdFileSize

from .queue import Slot


@dataclass(frozen=True, kw_only=True, slots=True)
class History(DataClassORJSONMixin):
    """Representation the history."""

    class Config(BaseConfig):
        """Mashumaro configuration."""

        serialization_strategy = {float: SABnzbdFileSize()}  # noqa: RUF012
        serialize_by_alias = True
        omit_none = True

    total_size: float
    month_size: float
    week_size: float
    day_size: float
    slots: list[Slot]
    ppslots: int
    noofslots: int
    last_history_update: int


@dataclass(frozen=True, kw_only=True, slots=True)
class HistoryResponse(DataClassORJSONMixin):
    """History API response."""

    history: History
