"""Alibaba Bailian Coding Plan and Token Plan (native Anthropic Messages API)."""

from __future__ import annotations

from providers.base import ProviderConfig
from providers.plan import AnthropicSubscriptionPlanTransport, normalize_with_suffix_map

from .models import coding_plan_model_infos, token_plan_model_infos

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
    return normalize_with_suffix_map(
        configured,
        default,
        legacy_map=_OPENAI_TO_ANTHROPIC_BASE,
    )


class _BailianAnthropicPlanTransport(AnthropicSubscriptionPlanTransport):
    """Shared Anthropic transport for Bailian subscription plans."""

    def __init__(
        self,
        config: ProviderConfig,
        *,
        provider_name: str,
        default_base_url: str,
        catalog,
    ):
        normalized = normalize_bailian_anthropic_base_url(
            config.base_url or "",
            default_base_url,
        )
        effective_config = config.model_copy(update={"base_url": normalized})
        super().__init__(
            effective_config,
            provider_name=provider_name,
            default_base_url=normalized,
            catalog=catalog,
            auth_style="x_api_key",
        )


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
