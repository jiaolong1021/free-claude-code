"""Kimi Code subscription (Anthropic-compatible Messages API)."""

from __future__ import annotations

from providers.plan import base_url_normalizer, plan_provider
from providers.plan.catalogs import KIMI_CODING_PLAN_MODEL_IDS

KIMI_CODING_PLAN_BASE_URL = "https://api.kimi.com/coding/v1"

_LEGACY_BASE_MAP: dict[str, str] = {
    "https://api.kimi.com/coding": KIMI_CODING_PLAN_BASE_URL,
}

normalize_kimi_coding_plan_base_url = base_url_normalizer(
    default=KIMI_CODING_PLAN_BASE_URL,
    legacy_map=_LEGACY_BASE_MAP,
)

KimiCodingPlanProvider = plan_provider(
    class_name="KimiCodingPlanProvider",
    provider_name="KIMI_CODING_PLAN",
    default_base_url=KIMI_CODING_PLAN_BASE_URL,
    model_ids=KIMI_CODING_PLAN_MODEL_IDS,
    legacy_base_map=_LEGACY_BASE_MAP,
    auth_style="bearer",
)
