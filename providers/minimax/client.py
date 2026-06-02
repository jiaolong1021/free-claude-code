"""MiniMax Token Plan (native Anthropic Messages API)."""

from __future__ import annotations

from providers.plan import base_url_normalizer, plan_provider
from providers.plan.catalogs import MINIMAX_TOKEN_PLAN_MODEL_IDS

MINIMAX_TOKEN_PLAN_BASE_URL = "https://api.minimax.io/anthropic/v1"

_LEGACY_BASE_MAP: dict[str, str] = {
    "https://api.minimax.io/v1": MINIMAX_TOKEN_PLAN_BASE_URL,
}

normalize_minimax_token_plan_base_url = base_url_normalizer(
    default=MINIMAX_TOKEN_PLAN_BASE_URL,
    legacy_map=_LEGACY_BASE_MAP,
)

MinimaxTokenPlanProvider = plan_provider(
    class_name="MinimaxTokenPlanProvider",
    provider_name="MINIMAX_TOKEN_PLAN",
    default_base_url=MINIMAX_TOKEN_PLAN_BASE_URL,
    model_ids=MINIMAX_TOKEN_PLAN_MODEL_IDS,
    legacy_base_map=_LEGACY_BASE_MAP,
    auth_style="bearer",
)
