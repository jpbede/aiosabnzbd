"""History models."""

from dataclasses import dataclass

from mashumaro.mixins.orjson import DataClassORJSONMixin

from .queue import Slot


@dataclass(frozen=True, kw_only=True, slots=True)
class History(DataClassORJSONMixin):
    """Representation the history."""

    total_size: str
    month_size: str
    week_size: str
    day_size: str
    slots: list[Slot]
    ppslots: int
    noofslots: int
    last_history_update: int


@dataclass(frozen=True, kw_only=True, slots=True)
class HistoryResponse(DataClassORJSONMixin):
    """History API response."""

    history: History
