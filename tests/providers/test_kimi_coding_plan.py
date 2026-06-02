"""Tests for Kimi Code (Coding Plan) provider."""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

import pytest

from providers.base import ProviderConfig
from providers.kimi import (
    KIMI_CODING_PLAN_BASE_URL,
    KimiCodingPlanProvider,
    normalize_kimi_coding_plan_base_url,
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


def test_normalize_maps_coding_root_without_v1():
    assert (
        normalize_kimi_coding_plan_base_url(
            "https://api.kimi.com/coding",
            KIMI_CODING_PLAN_BASE_URL,
        )
        == KIMI_CODING_PLAN_BASE_URL
    )


def test_request_headers_use_bearer_auth():
    provider = KimiCodingPlanProvider(
        ProviderConfig(api_key="kimi-code-test", base_url=KIMI_CODING_PLAN_BASE_URL)
    )
    headers = provider._request_headers()
    assert headers["Authorization"] == "Bearer kimi-code-test"
    assert "x-api-key" not in headers


@pytest.mark.asyncio
async def test_list_model_infos_uses_static_catalog():
    provider = KimiCodingPlanProvider(
        ProviderConfig(api_key="kimi-code-test", base_url=KIMI_CODING_PLAN_BASE_URL)
    )
    infos = await provider.list_model_infos()
    assert any(info.model_id == "kimi-for-coding" for info in infos)
