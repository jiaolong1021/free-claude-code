"""Tests for MiniMax Token Plan provider."""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

import pytest

from providers.base import ProviderConfig
from providers.minimax import (
    MINIMAX_TOKEN_PLAN_BASE_URL,
    MinimaxTokenPlanProvider,
    normalize_minimax_token_plan_base_url,
)


@pytest.fixture(autouse=True)
def mock_rate_limiter():
    @asynccontextmanager
    async def _slot():
        yield

    with patch("providers.anthropic_messages.GlobalRateLimiter") as mock:
        instance = mock.get_scoped_instance.return_value

        async def _passthrough(fn, *args, **kwargs):
            return await fn(*args, **kwargs)

        instance.execute_with_retry = AsyncMock(side_effect=_passthrough)
        instance.concurrency_slot.side_effect = _slot
        yield instance


def test_normalize_maps_anthropic_root_without_v1():
    assert (
        normalize_minimax_token_plan_base_url(
            "https://api.minimax.io/anthropic",
            MINIMAX_TOKEN_PLAN_BASE_URL,
        )
        == MINIMAX_TOKEN_PLAN_BASE_URL
    )


def test_request_headers_use_bearer_auth():
    provider = MinimaxTokenPlanProvider(
        ProviderConfig(api_key="minimax-test", base_url=MINIMAX_TOKEN_PLAN_BASE_URL)
    )
    headers = provider._request_headers()
    assert headers["Authorization"] == "Bearer minimax-test"
    assert "x-api-key" not in headers


@pytest.mark.asyncio
async def test_list_model_infos_uses_static_catalog():
    provider = MinimaxTokenPlanProvider(
        ProviderConfig(api_key="minimax-test", base_url=MINIMAX_TOKEN_PLAN_BASE_URL)
    )
    infos = await provider.list_model_infos()
    assert any(info.model_id == "MiniMax-M2.5" for info in infos)
