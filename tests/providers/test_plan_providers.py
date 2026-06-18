"""Shared tests for CN subscription plan providers."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from providers.base import ProviderConfig
from providers.kimi import KIMI_CODING_PLAN_BASE_URL, KimiCodingPlanProvider
from providers.minimax import MINIMAX_TOKEN_PLAN_BASE_URL, MinimaxTokenPlanProvider
from providers.volcengine import (
    VOLCENGINE_CODING_PLAN_BASE_URL,
    VolcengineCodingPlanProvider,
)
from providers.zhipu import ZHIPU_CODING_PLAN_BASE_URL, ZhipuCodingPlanProvider


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


@pytest.mark.parametrize(
    ("provider_cls", "base_url", "api_key", "sample_model", "auth_header"),
    [
        (
            VolcengineCodingPlanProvider,
            VOLCENGINE_CODING_PLAN_BASE_URL,
            "volc-test",
            "ark-code-latest",
            ("x-api-key", "volc-test"),
        ),
        (
            ZhipuCodingPlanProvider,
            ZHIPU_CODING_PLAN_BASE_URL,
            "zhipu-test",
            "glm-5.1",
            ("x-api-key", "zhipu-test"),
        ),
        (
            KimiCodingPlanProvider,
            KIMI_CODING_PLAN_BASE_URL,
            "kimi-code-test",
            "kimi-for-coding",
            ("Authorization", "Bearer kimi-code-test"),
        ),
        (
            MinimaxTokenPlanProvider,
            MINIMAX_TOKEN_PLAN_BASE_URL,
            "minimax-test",
            "MiniMax-M2.5",
            ("Authorization", "Bearer minimax-test"),
        ),
    ],
)
@pytest.mark.asyncio
async def test_plan_provider_init_catalog_and_headers(
    provider_cls: type[Any],
    base_url: str,
    api_key: str,
    sample_model: str,
    auth_header: tuple[str, str],
):
    provider = provider_cls(ProviderConfig(api_key=api_key, base_url=base_url))
    assert provider._api_key == api_key
    assert provider._base_url == base_url

    infos = await provider.list_model_infos()
    assert any(info.model_id == sample_model for info in infos)

    headers = provider._request_headers()
    header_name, header_value = auth_header
    assert headers[header_name] == header_value
