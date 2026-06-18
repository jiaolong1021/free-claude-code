"""Tests for the custom Anthropic-compatible endpoint provider."""

from __future__ import annotations

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

import pytest

from providers.base import ProviderConfig
from providers.custom_anthropic import CustomAnthropicProvider
from providers.exceptions import AuthenticationError
from providers.registry import (
    PROVIDER_DESCRIPTORS,
    build_provider_config,
    create_provider,
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


def test_custom_anthropic_preserves_configured_base_url():
    custom = "https://proxy.example.com/api/coding/v1"
    provider = CustomAnthropicProvider(
        ProviderConfig(api_key="custom-key", base_url=custom),
        model_ids=frozenset({"ark-code-latest"}),
    )

    assert provider._base_url == custom
    assert provider._api_key == "custom-key"


@pytest.mark.asyncio
async def test_custom_anthropic_lists_configured_models():
    provider = CustomAnthropicProvider(
        ProviderConfig(
            api_key="custom-key",
            base_url="https://proxy.example.com/api/coding/v1",
        ),
        model_ids=frozenset({"ark-code-latest", "glm-4.7"}),
    )

    infos = await provider.list_model_infos()
    model_ids = {info.model_id for info in infos}
    assert model_ids == {"ark-code-latest", "glm-4.7"}


@pytest.mark.parametrize(
    ("auth_style", "header_name", "header_value"),
    [
        ("x_api_key", "x-api-key", "custom-key"),
        ("bearer", "Authorization", "Bearer custom-key"),
    ],
)
def test_custom_anthropic_request_headers(auth_style, header_name, header_value):
    provider = CustomAnthropicProvider(
        ProviderConfig(
            api_key="custom-key",
            base_url="https://proxy.example.com/api/coding/v1",
        ),
        model_ids=frozenset(),
        auth_style=auth_style,
    )

    headers = provider._request_headers()
    assert headers[header_name] == header_value


def test_create_custom_anthropic_requires_base_url():
    settings = _make_settings(
        custom_anthropic_api_key="custom-key",
        custom_anthropic_base_url="",
        model="custom_anthropic/ark-code-latest",
        configured_chat_model_refs=lambda: (
            _configured_ref("custom_anthropic/ark-code-latest"),
        ),
    )

    with pytest.raises(AuthenticationError, match="CUSTOM_ANTHROPIC_BASE_URL"):
        create_provider("custom_anthropic", settings)


def test_create_custom_anthropic_uses_configured_models():
    ref = _configured_ref("custom_anthropic/ark-code-latest")
    settings = _make_settings(
        custom_anthropic_api_key="custom-key",
        custom_anthropic_base_url="https://proxy.example.com/api/coding/v1",
        model="custom_anthropic/ark-code-latest",
        configured_chat_model_refs=lambda: (ref,),
    )

    provider = create_provider("custom_anthropic", settings)
    assert isinstance(provider, CustomAnthropicProvider)
    assert provider._base_url == "https://proxy.example.com/api/coding/v1"


def test_build_provider_config_allows_empty_custom_base_url():
    config = build_provider_config(
        PROVIDER_DESCRIPTORS["custom_anthropic"],
        _make_settings(
            custom_anthropic_api_key="custom-key",
            custom_anthropic_base_url="",
        ),
    )

    assert config.api_key == "custom-key"
    assert config.base_url in ("", None)


def _configured_ref(model_ref: str):
    from config.settings import ConfiguredChatModelRef, Settings

    return ConfiguredChatModelRef(
        model_ref=model_ref,
        provider_id=Settings.parse_provider_type(model_ref),
        model_id=Settings.parse_model_name(model_ref),
        sources=("MODEL",),
    )


def _make_settings(**overrides):
    from unittest.mock import MagicMock

    mock = MagicMock()
    mock.model = overrides.get("model", "nvidia_nim/meta/llama3")
    mock.custom_anthropic_api_key = overrides.get("custom_anthropic_api_key", "")
    mock.custom_anthropic_base_url = overrides.get("custom_anthropic_base_url", "")
    mock.custom_anthropic_auth_style = overrides.get(
        "custom_anthropic_auth_style", "x_api_key"
    )
    mock.custom_anthropic_proxy = ""
    mock.provider_rate_limit = 40
    mock.provider_rate_window = 60
    mock.provider_max_concurrency = 5
    mock.http_read_timeout = 300.0
    mock.http_write_timeout = 10.0
    mock.http_connect_timeout = 10.0
    mock.enable_model_thinking = True
    mock.log_raw_sse_events = False
    mock.log_api_error_tracebacks = False
    mock.configured_chat_model_refs = overrides.get(
        "configured_chat_model_refs", lambda: ()
    )
    for key, value in overrides.items():
        setattr(mock, key, value)
    return mock
