"""Zhipu GLM Coding Plan (native Anthropic Messages API)."""

from __future__ import annotations

from providers.base import ProviderConfig
from providers.plan import AnthropicSubscriptionPlanTransport, normalize_with_suffix_map

from .models import coding_plan_model_infos

ZHIPU_CODING_PLAN_BASE_URL = "https://open.bigmodel.cn/api/anthropic/v1"

_LEGACY_BASE_MAP: dict[str, str] = {
    "https://open.bigmodel.cn/api/coding/paas/v4": ZHIPU_CODING_PLAN_BASE_URL,
    "https://open.bigmodel.cn/api/paas/v4": ZHIPU_CODING_PLAN_BASE_URL,
}


def normalize_zhipu_coding_plan_base_url(configured: str, default: str) -> str:
    return normalize_with_suffix_map(
        configured,
        default,
        legacy_map=_LEGACY_BASE_MAP,
    )


class ZhipuCodingPlanProvider(AnthropicSubscriptionPlanTransport):
    """Zhipu GLM Coding Plan via Anthropic-compatible Messages API."""

    def __init__(self, config: ProviderConfig):
        normalized = normalize_zhipu_coding_plan_base_url(
            config.base_url or "",
            ZHIPU_CODING_PLAN_BASE_URL,
        )
        effective_config = config.model_copy(update={"base_url": normalized})
        super().__init__(
            effective_config,
            provider_name="ZHIPU_CODING_PLAN",
            default_base_url=normalized,
            catalog=coding_plan_model_infos,
            auth_style="x_api_key",
        )
