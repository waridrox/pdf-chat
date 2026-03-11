"""Conftest override for unit tests — disables the DB lifecycle fixture."""

import pytest_asyncio


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _session_db_lifecycle():
    """No-op override: unit tests don't need a database."""
    yield
