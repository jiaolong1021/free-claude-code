"""Alibaba Bailian Coding Plan and Token Plan (native Anthropic Messages API)."""

from __future__ import annotations

from providers.plan import base_url_normalizer, plan_provider
from providers.plan.catalogs import (
    BAILIAN_CODING_PLAN_MODEL_IDS,
    BAILIAN_TOKEN_PLAN_MODEL_IDS,
)

# Docs advertise ``.../apps/anthropic``; upstream expects ``.../apps/anthropic/v1/messages``.
BAILIAN_CODING_PLAN_BASE_URL = "https://coding.dashscope.aliyuncs.com/apps/anthropic/v1"
BAILIAN_CODING_PLAN_INTL_BASE_URL = (
    "https://coding-intl.dashscope.aliyuncs.com/apps/anthropic/v1"
)
BAILIAN_TOKEN_PLAN_BASE_URL = (
    "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1"
)

_LEGACY_BASE_MAP: dict[str, str] = {
    "https://coding.dashscope.aliyuncs.com/v1": BAILIAN_CODING_PLAN_BASE_URL,
    "https://coding-intl.dashscope.aliyuncs.com/v1": BAILIAN_CODING_PLAN_INTL_BASE_URL,
    "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1": (
        BAILIAN_TOKEN_PLAN_BASE_URL
    ),
}

normalize_bailian_anthropic_base_url = base_url_normalizer(
    default=BAILIAN_CODING_PLAN_BASE_URL,
    legacy_map=_LEGACY_BASE_MAP,
)

BailianCodingPlanProvider = plan_provider(
    class_name="BailianCodingPlanProvider",
    provider_name="BAILIAN_CODING_PLAN",
    default_base_url=BAILIAN_CODING_PLAN_BASE_URL,
    model_ids=BAILIAN_CODING_PLAN_MODEL_IDS,
    legacy_base_map=_LEGACY_BASE_MAP,
)

BailianTokenPlanProvider = plan_provider(
    class_name="BailianTokenPlanProvider",
    provider_name="BAILIAN_TOKEN_PLAN",
    default_base_url=BAILIAN_TOKEN_PLAN_BASE_URL,
    model_ids=BAILIAN_TOKEN_PLAN_MODEL_IDS,
    legacy_base_map=_LEGACY_BASE_MAP,
)
