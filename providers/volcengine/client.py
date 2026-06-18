"""Volcengine Ark Coding Plan (native Anthropic Messages API)."""

from __future__ import annotations

from providers.plan import base_url_normalizer, plan_provider
from providers.plan.catalogs import VOLCENGINE_CODING_PLAN_MODEL_IDS

VOLCENGINE_CODING_PLAN_BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v1"

_LEGACY_BASE_MAP: dict[str, str] = {
    "https://ark.cn-beijing.volces.com/api/coding/v3": VOLCENGINE_CODING_PLAN_BASE_URL,
}

normalize_volcengine_coding_plan_base_url = base_url_normalizer(
    default=VOLCENGINE_CODING_PLAN_BASE_URL,
    legacy_map=_LEGACY_BASE_MAP,
)

VolcengineCodingPlanProvider = plan_provider(
    class_name="VolcengineCodingPlanProvider",
    provider_name="VOLCENGINE_CODING_PLAN",
    default_base_url=VOLCENGINE_CODING_PLAN_BASE_URL,
    model_ids=VOLCENGINE_CODING_PLAN_MODEL_IDS,
    legacy_base_map=_LEGACY_BASE_MAP,
)
