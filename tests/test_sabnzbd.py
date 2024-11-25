"""Tests for the SABnzbd client."""

from aioresponses import aioresponses
import pytest
from syrupy.assertion import SnapshotAssertion

from aiosabnzbd import (
    QueueOperationCommand,
    SABnzbdClient,
    SABnzbdConnectionError,
    SABnzbdConnectionTimeoutError,
    SABnzbdInvalidAPIKeyError,
    SABnzbdMissingAPIKeyError,
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

    async with SABnzbdClient(url="http://localhost:8080", api_key="ab123") as c:
        assert await c.queue() == snapshot
        assert c.session is not None

    assert c.session.closed


async def test_catch_connection_error(
    client: SABnzbdClient, responses: aioresponses
) -> None:
    """Test JSON response is handled correctly with given session."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=queue",
        status=500,
        headers={"Content-Type": "application/json"},
        body="Boooom!",
    )
    with pytest.raises(SABnzbdConnectionError):
        await client.queue()


async def test_timeout(
    client: SABnzbdClient,
    responses: aioresponses,
) -> None:
    """Test request timeout."""
    responses.add(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=queue",
        timeout=True,
    )
    with pytest.raises(SABnzbdConnectionTimeoutError):
        await client.queue()


async def test_queue(
    client: SABnzbdClient, responses: aioresponses, snapshot: SnapshotAssertion
) -> None:
    """Test getting the queue."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=queue",
        body=load_fixture("queue.json"),
    )

    assert snapshot == await client.queue()


async def test_operate_queue(client: SABnzbdClient, responses: aioresponses) -> None:
    """Test operating the queue."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=pause",
        body='{"status": true}',
    )

    response = await client.operate_queue(command=QueueOperationCommand.PAUSE)

    assert response == StatusResponse(status=True)


async def test_missing_api_key(client: SABnzbdClient, responses: aioresponses) -> None:
    """Test missing API key."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=queue",
        body="API Key Required",
    )

    with pytest.raises(SABnzbdMissingAPIKeyError):
        await client.queue()


async def test_invalid_api_key(client: SABnzbdClient, responses: aioresponses) -> None:
    """Test invalid API key."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=queue",
        body="API Key Incorrect",
    )

    with pytest.raises(SABnzbdInvalidAPIKeyError):
        await client.queue()


async def test_set_speed_limit(client: SABnzbdClient, responses: aioresponses) -> None:
    """Test setting speed limit."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=config&name=speedlimit&value=50",
        body='{"status": true}',
    )

    response = await client.set_speed_limit(percentage=50)

    assert response == StatusResponse(status=True)


async def test_history(
    client: SABnzbdClient, responses: aioresponses, snapshot: SnapshotAssertion
) -> None:
    """Test getting the queue."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=history",
        body=load_fixture("history.json"),
    )

    assert snapshot == await client.history()


async def test_version(client: SABnzbdClient, responses: aioresponses) -> None:
    """Test getting the version."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=version",
        body='{"version": "3.0.0"}',
    )

    assert await client.version() == "3.0.0"


async def test_combined_queue_history(
    client: SABnzbdClient, responses: aioresponses, snapshot: SnapshotAssertion
) -> None:
    """Test getting the queue and history."""
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=queue",
        body=load_fixture("queue.json"),
    )
    responses.get(
        "http://localhost:8080/api?apikey=abc123&output=json&mode=history",
        body=load_fixture("history.json"),
    )

    assert snapshot == await client.combined_queue_history()
