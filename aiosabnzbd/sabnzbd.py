"""Async Python client for SABnzbd."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import logging
import socket
from typing import TYPE_CHECKING, Self

from aiohttp import ClientError, ClientSession
from yarl import URL

from .exceptions import (
    SABnzbdConnectionError,
    SABnzbdConnectionTimeoutError,
    SABnzbdInvalidAPIKeyError,
    SABnzbdMissingAPIKeyError,
)
from .models import History, HistoryResponse
from .models.base import CombinedQueueHistory, SABnzbdRequest
from .models.queue import Queue, QueueResponse
from .models.status import StatusResponse, VersionResponse

if TYPE_CHECKING:
    from .const import QueueOperationCommand

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True)
class SABnzbdClient:
    """SABnzbd API client."""

    url: str
    api_key: str
    path: str = "/api"
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(self, request: SABnzbdRequest) -> str:
        """Execute a GET request against the API."""
        url = URL(self.url).with_path(self.path)

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        request_params = request.query_params
        _LOGGER.debug("Doing request: GET %s %s", url, request_params)

        params = {
            "output": "json",
            "apikey": self.api_key,
        }
        params.update(request_params)

        try:
            async with self.session.get(
                url,
                params=params,
            ) as response:
                response.raise_for_status()
                response_text = await response.text()
        except TimeoutError as exception:
            msg = "Timeout occurred while connecting to the SABnzbd API"
            raise SABnzbdConnectionTimeoutError(msg) from exception
        except (
            ClientError,
            socket.gaierror,
        ) as exception:
            msg = "Error occurred while communicating to the SABnzbd API"
            raise SABnzbdConnectionError(msg) from exception

        if response_text == "API Key Incorrect":
            msg = "API Key is invalid"
            raise SABnzbdInvalidAPIKeyError(msg)

        if response_text == "API Key Required":
            msg = "API Key is required"
            raise SABnzbdMissingAPIKeyError(msg)

        _LOGGER.debug(
            "Got response with status %s and body: %s",
            response.status,
            response_text,
        )

        return response_text

    async def history(
        self,
    ) -> History:
        """Get current history."""
        result = await self._request(
            SABnzbdRequest(
                mode="history",
            ),
        )

        return HistoryResponse.from_json(result).history

    async def queue(
        self,
    ) -> Queue:
        """Get current queue status."""
        result = await self._request(
            SABnzbdRequest(
                mode="queue",
            ),
        )

        return QueueResponse.from_json(result).queue

    async def operate_queue(self, *, command: QueueOperationCommand) -> StatusResponse:
        """Operate the queue."""
        result = await self._request(
            SABnzbdRequest(mode=command),
        )
        return StatusResponse.from_json(result)

    async def set_speed_limit(self, *, percentage: int) -> StatusResponse:
        """Set the speed limit."""
        result = await self._request(
            SABnzbdRequest(
                mode="config",
                name="speedlimit",
                value=percentage,
            ),
        )
        return StatusResponse.from_json(result)

    async def version(self) -> str:
        """Get the version of the SABnzbd instance."""
        result = await self._request(
            SABnzbdRequest(
                mode="version",
            ),
        )

        return VersionResponse.from_json(result).version

    async def combined_queue_history(self) -> CombinedQueueHistory:
        """Get the combined queue and history."""
        queue, history = await asyncio.gather(
            self.queue(),
            self.history(),
        )
        return CombinedQueueHistory(queue=queue, history=history)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit."""
        await self.close()
