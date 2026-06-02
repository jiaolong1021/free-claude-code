"""Volcengine Ark Coding Plan (native Anthropic Messages API)."""

from __future__ import annotations

from providers.base import ProviderConfig
from providers.plan import AnthropicSubscriptionPlanTransport, normalize_with_suffix_map

from .models import coding_plan_model_infos

# Claude Code uses ``.../api/coding``; upstream expects ``.../api/coding/v1/messages``.
VOLCENGINE_CODING_PLAN_BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v1"

_LEGACY_BASE_MAP: dict[str, str] = {
    "https://ark.cn-beijing.volces.com/api/coding/v3": VOLCENGINE_CODING_PLAN_BASE_URL,
}


def normalize_volcengine_coding_plan_base_url(configured: str, default: str) -> str:
    return normalize_with_suffix_map(
        configured,
        default,
        legacy_map=_LEGACY_BASE_MAP,
    )


class VolcengineCodingPlanProvider(AnthropicSubscriptionPlanTransport):
    """Volcengine Ark Coding Plan via Anthropic-compatible Messages API."""

    def __init__(self, config: ProviderConfig):
        normalized = normalize_volcengine_coding_plan_base_url(
            config.base_url or "",
            VOLCENGINE_CODING_PLAN_BASE_URL,
        )
        effective_config = config.model_copy(update={"base_url": normalized})
        super().__init__(
            effective_config,
            provider_name="VOLCENGINE_CODING_PLAN",
            default_base_url=normalized,
            catalog=coding_plan_model_infos,
            auth_style="x_api_key",
        )
