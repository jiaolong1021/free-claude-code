"""Alibaba Bailian Coding Plan and Token Plan (native Anthropic Messages API)."""

from __future__ import annotations

from collections.abc import Callable

from providers.anthropic_messages import AnthropicMessagesTransport
from providers.base import ProviderConfig
from providers.model_listing import ProviderModelInfo

from .models import coding_plan_model_infos, token_plan_model_infos

_ANTHROPIC_VERSION = "2023-06-01"

# Docs advertise ``.../apps/anthropic``; upstream expects ``.../apps/anthropic/v1/messages``.
BAILIAN_CODING_PLAN_BASE_URL = "https://coding.dashscope.aliyuncs.com/apps/anthropic/v1"
BAILIAN_CODING_PLAN_INTL_BASE_URL = (
    "https://coding-intl.dashscope.aliyuncs.com/apps/anthropic/v1"
)
BAILIAN_TOKEN_PLAN_BASE_URL = (
    "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1"
)

# Legacy OpenAI-compatible defaults users may still have in .env.
_OPENAI_TO_ANTHROPIC_BASE: dict[str, str] = {
    "https://coding.dashscope.aliyuncs.com/v1": BAILIAN_CODING_PLAN_BASE_URL,
    "https://coding-intl.dashscope.aliyuncs.com/v1": BAILIAN_CODING_PLAN_INTL_BASE_URL,
    "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1": (
        BAILIAN_TOKEN_PLAN_BASE_URL
    ),
}


def normalize_bailian_anthropic_base_url(configured: str, default: str) -> str:
    """Map plan Base URLs to the Anthropic Messages root (with ``/v1`` suffix)."""
    base = (configured or default).rstrip("/")
    mapped = _OPENAI_TO_ANTHROPIC_BASE.get(base)
    if mapped is not None:
        return mapped
    if base.endswith("/apps/anthropic"):
        return f"{base}/v1"
    return base


class _BailianAnthropicPlanTransport(AnthropicMessagesTransport):
    """Shared Anthropic transport for Bailian subscription plans."""

    def __init__(
        self,
        config: ProviderConfig,
        *,
        provider_name: str,
        default_base_url: str,
        catalog: Callable[[], frozenset[ProviderModelInfo]],
    ):
        self._catalog = catalog
        normalized = normalize_bailian_anthropic_base_url(
            config.base_url or "",
            default_base_url,
        )
        effective_config = config.model_copy(update={"base_url": normalized})
        super().__init__(
            effective_config,
            provider_name=provider_name,
            default_base_url=normalized,
        )

    async def list_model_infos(self) -> frozenset[ProviderModelInfo]:
        """Plans do not expose a working OpenAI-style ``GET /models`` listing."""
        return self._catalog()

    def _request_headers(self) -> dict[str, str]:
        # DashScope Anthropic-compatible endpoints expect ``x-api-key`` (not only Bearer).
        return {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
            "anthropic-version": _ANTHROPIC_VERSION,
            "x-api-key": self._api_key,
        }


class BailianCodingPlanProvider(_BailianAnthropicPlanTransport):
    """Bailian Coding Plan (sk-sp-*) via Anthropic-compatible Messages API."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="BAILIAN_CODING_PLAN",
            default_base_url=BAILIAN_CODING_PLAN_BASE_URL,
            catalog=coding_plan_model_infos,
        )


class BailianTokenPlanProvider(_BailianAnthropicPlanTransport):
    """Bailian Token Plan team edition via Anthropic-compatible Messages API."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="BAILIAN_TOKEN_PLAN",
            default_base_url=BAILIAN_TOKEN_PLAN_BASE_URL,
            catalog=token_plan_model_infos,
        )
