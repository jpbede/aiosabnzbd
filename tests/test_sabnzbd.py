"""Tests for the Sabnzbd client."""
from aioresponses import aioresponses
import pytest
from syrupy.assertion import SnapshotAssertion

from aiosabnzbd import (
    QueueOperationCommand,
    Sabnzbd,
    SabnzbdConnectionError,
    SabnzbdConnectionTimeoutError,
    StatusResponse,
)

from . import load_fixture


async def test_json_request_without_session(
    snapshot: SnapshotAssertion, responses: aioresponses
) -> None:
    """Test JSON response is handled correctly without given session."""
    responses.get(
        "http://localhost:8080/api?apikey=ab123&mode=queue&output=json",
        body=load_fixture("queue.json"),
    )

    async with Sabnzbd(host="localhost", port=8080, api_key="ab123") as c:
        assert await c.queue() == snapshot
        assert c.session is not None

    assert c.session.closed


async def test_catch_connection_error(client: Sabnzbd, responses: aioresponses) -> None:
    """Test JSON response is handled correctly with given session."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=queue",
        status=500,
        headers={"Content-Type": "application/json"},
        body="Boooom!",
    )
    with pytest.raises(SabnzbdConnectionError):
        await client.queue()


async def test_timeout(
    client: Sabnzbd,
    responses: aioresponses,
) -> None:
    """Test request timeout."""
    responses.add(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=queue",
        timeout=True,
    )
    with pytest.raises(SabnzbdConnectionTimeoutError):
        await client.queue()


async def test_queue(
    client: Sabnzbd, responses: aioresponses, snapshot: SnapshotAssertion
) -> None:
    """Test getting the queue."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=queue",
        body=load_fixture("queue.json"),
    )

    assert snapshot == await client.queue()


async def test_operate_queue(client: Sabnzbd, responses: aioresponses) -> None:
    """Test operating the queue."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=pause",
        body='{"status": true}',
    )

    response = await client.operate_queue(command=QueueOperationCommand.PAUSE)

    assert response == StatusResponse(status=True)
