"""Tests for Volcengine Ark Coding Plan provider."""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from api.models.anthropic import Message, MessagesRequest
from providers.base import ProviderConfig
from providers.volcengine import (
    VOLCENGINE_CODING_PLAN_BASE_URL,
    VolcengineCodingPlanProvider,
    normalize_volcengine_coding_plan_base_url,
)


class FakeResponse:
    def __init__(self, *, status_code=200, lines=None):
        self.status_code = status_code
        self._lines = lines or []
        self.is_closed = False

    async def aiter_lines(self):
        for line in self._lines:
            yield line

    async def aclose(self):
        self.is_closed = True

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


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
        normalize_volcengine_coding_plan_base_url(
            "https://ark.cn-beijing.volces.com/api/coding",
            VOLCENGINE_CODING_PLAN_BASE_URL,
        )
        == VOLCENGINE_CODING_PLAN_BASE_URL
    )


def test_init_uses_anthropic_messages_base():
    provider = VolcengineCodingPlanProvider(
        ProviderConfig(api_key="volc-test", base_url=VOLCENGINE_CODING_PLAN_BASE_URL)
    )
    assert provider._api_key == "volc-test"
    assert provider._base_url == VOLCENGINE_CODING_PLAN_BASE_URL


@pytest.mark.asyncio
async def test_list_model_infos_uses_static_catalog():
    provider = VolcengineCodingPlanProvider(
        ProviderConfig(api_key="volc-test", base_url=VOLCENGINE_CODING_PLAN_BASE_URL)
    )
    infos = await provider.list_model_infos()
    assert any(info.model_id == "ark-code-latest" for info in infos)


def test_request_headers_use_x_api_key():
    provider = VolcengineCodingPlanProvider(
        ProviderConfig(api_key="volc-test", base_url=VOLCENGINE_CODING_PLAN_BASE_URL)
    )
    headers = provider._request_headers()
    assert headers["x-api-key"] == "volc-test"
    assert "Authorization" not in headers


@pytest.mark.asyncio
async def test_stream_posts_to_messages_path():
    provider = VolcengineCodingPlanProvider(
        ProviderConfig(api_key="volc-test", base_url=VOLCENGINE_CODING_PLAN_BASE_URL)
    )
    request = MessagesRequest(
        model="ark-code-latest",
        messages=[Message(role="user", content="hi")],
    )
    response = FakeResponse(
        lines=[
            "event: message_start",
            'data: {"type":"message_start"}',
            "",
        ]
    )

    with (
        patch.object(
            provider._client, "build_request", return_value=MagicMock()
        ) as mock_build,
        patch.object(
            provider._client,
            "send",
            new_callable=AsyncMock,
            return_value=response,
        ),
    ):
        events = [event async for event in provider.stream_response(request)]

    assert events
    assert mock_build.call_args.args[:2] == ("POST", "/messages")
