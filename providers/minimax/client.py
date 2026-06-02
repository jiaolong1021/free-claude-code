"""MiniMax Token Plan (native Anthropic Messages API)."""

from __future__ import annotations

from providers.base import ProviderConfig
from providers.plan import AnthropicSubscriptionPlanTransport, normalize_with_suffix_map

from .models import token_plan_model_infos

MINIMAX_TOKEN_PLAN_BASE_URL = "https://api.minimax.io/anthropic/v1"

_LEGACY_BASE_MAP: dict[str, str] = {
    "https://api.minimax.io/v1": MINIMAX_TOKEN_PLAN_BASE_URL,
}


def normalize_minimax_token_plan_base_url(configured: str, default: str) -> str:
    return normalize_with_suffix_map(
        configured,
        default,
        legacy_map=_LEGACY_BASE_MAP,
    )


class MinimaxTokenPlanProvider(AnthropicSubscriptionPlanTransport):
    """MiniMax Token Plan subscription via Anthropic-compatible Messages API."""

    def __init__(self, config: ProviderConfig):
        normalized = normalize_minimax_token_plan_base_url(
            config.base_url or "",
            MINIMAX_TOKEN_PLAN_BASE_URL,
        )
        effective_config = config.model_copy(update={"base_url": normalized})
        super().__init__(
            effective_config,
            provider_name="MINIMAX_TOKEN_PLAN",
            default_base_url=normalized,
            catalog=token_plan_model_infos,
            auth_style="bearer",
        )
