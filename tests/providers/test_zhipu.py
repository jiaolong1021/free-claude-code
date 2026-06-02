"""Tests for Zhipu GLM Coding Plan provider."""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

import pytest

from providers.base import ProviderConfig
from providers.zhipu import (
    ZHIPU_CODING_PLAN_BASE_URL,
    ZhipuCodingPlanProvider,
    normalize_zhipu_coding_plan_base_url,
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


def test_normalize_maps_openai_coding_endpoint():
    assert (
        normalize_zhipu_coding_plan_base_url(
            "https://open.bigmodel.cn/api/coding/paas/v4",
            ZHIPU_CODING_PLAN_BASE_URL,
        )
        == ZHIPU_CODING_PLAN_BASE_URL
    )


def test_normalize_maps_anthropic_root_without_v1():
    assert (
        normalize_zhipu_coding_plan_base_url(
            "https://open.bigmodel.cn/api/anthropic",
            ZHIPU_CODING_PLAN_BASE_URL,
        )
        == ZHIPU_CODING_PLAN_BASE_URL
    )


@pytest.mark.asyncio
async def test_list_model_infos_uses_static_catalog():
    provider = ZhipuCodingPlanProvider(
        ProviderConfig(api_key="zhipu-test", base_url=ZHIPU_CODING_PLAN_BASE_URL)
    )
    infos = await provider.list_model_infos()
    assert any(info.model_id == "glm-5.1" for info in infos)
