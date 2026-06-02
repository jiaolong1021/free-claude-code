"""Zhipu GLM Coding Plan (native Anthropic Messages API)."""

from __future__ import annotations

from providers.plan import base_url_normalizer, plan_provider
from providers.plan.catalogs import ZHIPU_CODING_PLAN_MODEL_IDS

ZHIPU_CODING_PLAN_BASE_URL = "https://open.bigmodel.cn/api/anthropic/v1"

_LEGACY_BASE_MAP: dict[str, str] = {
    "https://open.bigmodel.cn/api/coding/paas/v4": ZHIPU_CODING_PLAN_BASE_URL,
    "https://open.bigmodel.cn/api/paas/v4": ZHIPU_CODING_PLAN_BASE_URL,
}

normalize_zhipu_coding_plan_base_url = base_url_normalizer(
    default=ZHIPU_CODING_PLAN_BASE_URL,
    legacy_map=_LEGACY_BASE_MAP,
)

ZhipuCodingPlanProvider = plan_provider(
    class_name="ZhipuCodingPlanProvider",
    provider_name="ZHIPU_CODING_PLAN",
    default_base_url=ZHIPU_CODING_PLAN_BASE_URL,
    model_ids=ZHIPU_CODING_PLAN_MODEL_IDS,
    legacy_base_map=_LEGACY_BASE_MAP,
)
