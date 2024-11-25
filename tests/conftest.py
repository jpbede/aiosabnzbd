"""Fixtures for aiosabnzbd tests."""

from collections.abc import AsyncGenerator, Generator

import aiohttp
from aioresponses import aioresponses
import pytest

from aiosabnzbd import SABnzbdClient


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses


@pytest.fixture(name="client")
async def client() -> AsyncGenerator[SABnzbdClient, None]:
    """Return a Sabnzbd client."""
    async with (
        aiohttp.ClientSession() as session,
        SABnzbdClient(
            host="localhost",
            port=8080,
            api_key="abc123",
            session=session,
        ) as sab_client,
    ):
        yield sab_client
