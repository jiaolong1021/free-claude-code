"""Kimi Code subscription (Anthropic-compatible Messages API)."""

from __future__ import annotations

from providers.base import ProviderConfig
from providers.plan import AnthropicSubscriptionPlanTransport, normalize_with_suffix_map

from .models import coding_plan_model_infos

KIMI_CODING_PLAN_BASE_URL = "https://api.kimi.com/coding/v1"

_LEGACY_BASE_MAP: dict[str, str] = {
    "https://api.kimi.com/coding": KIMI_CODING_PLAN_BASE_URL,
}


def normalize_kimi_coding_plan_base_url(configured: str, default: str) -> str:
    return normalize_with_suffix_map(
        configured,
        default,
        legacy_map=_LEGACY_BASE_MAP,
    )


class KimiCodingPlanProvider(AnthropicSubscriptionPlanTransport):
    """Kimi Code subscription via Anthropic-compatible Messages API."""

    def __init__(self, config: ProviderConfig):
        normalized = normalize_kimi_coding_plan_base_url(
            config.base_url or "",
            KIMI_CODING_PLAN_BASE_URL,
        )
        effective_config = config.model_copy(update={"base_url": normalized})
        super().__init__(
            effective_config,
            provider_name="KIMI_CODING_PLAN",
            default_base_url=normalized,
            catalog=coding_plan_model_infos,
            auth_style="bearer",
        )
