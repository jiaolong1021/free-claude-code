"""Tests for Alibaba Bailian Anthropic Messages providers."""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from api.models.anthropic import Message, MessagesRequest
from providers.bailian import (
    BAILIAN_CODING_PLAN_BASE_URL,
    BAILIAN_TOKEN_PLAN_BASE_URL,
    BailianCodingPlanProvider,
    BailianTokenPlanProvider,
)
from providers.base import ProviderConfig


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


@pytest.mark.parametrize(
    ("provider_cls", "expected_base", "api_key"),
    [
        (BailianCodingPlanProvider, BAILIAN_CODING_PLAN_BASE_URL, "sk-sp-test"),
        (BailianTokenPlanProvider, BAILIAN_TOKEN_PLAN_BASE_URL, "token-plan-test"),
    ],
)
def test_init_uses_anthropic_messages_base(provider_cls, expected_base, api_key):
    config = ProviderConfig(api_key=api_key, base_url=expected_base)
    provider = provider_cls(config)
    assert provider._api_key == api_key
    assert provider._base_url == expected_base


def test_coding_plan_legacy_env_openai_base_url_is_upgraded():
    config = ProviderConfig(
        api_key="sk-sp-test",
        base_url="https://coding.dashscope.aliyuncs.com/v1",
    )
    provider = BailianCodingPlanProvider(config)
    assert provider._base_url == BAILIAN_CODING_PLAN_BASE_URL


@pytest.mark.asyncio
async def test_list_model_infos_uses_static_catalog():
    provider = BailianCodingPlanProvider(
        ProviderConfig(api_key="sk-sp-test", base_url=BAILIAN_CODING_PLAN_BASE_URL)
    )
    infos = await provider.list_model_infos()
    assert any(info.model_id == "qwen3-coder-plus" for info in infos)


def test_request_headers_use_x_api_key_and_anthropic_version():
    provider = BailianCodingPlanProvider(
        ProviderConfig(api_key="sk-sp-test", base_url=BAILIAN_CODING_PLAN_BASE_URL)
    )
    headers = provider._request_headers()
    assert headers["x-api-key"] == "sk-sp-test"
    assert "Authorization" not in headers
    assert headers["anthropic-version"] == "2023-06-01"
    assert headers["Accept"] == "text/event-stream"


@pytest.mark.asyncio
async def test_stream_posts_to_messages_path():
    provider = BailianCodingPlanProvider(
        ProviderConfig(api_key="sk-sp-test", base_url=BAILIAN_CODING_PLAN_BASE_URL)
    )
    request = MessagesRequest(
        model="qwen3-coder-plus",
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
    assert mock_build.call_args.kwargs["headers"]["x-api-key"] == "sk-sp-test"
