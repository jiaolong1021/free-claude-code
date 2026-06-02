"""Static model catalogs for Volcengine Ark Coding Plan."""

from __future__ import annotations

from providers.model_listing import ProviderModelInfo, model_infos_from_ids

VOLCENGINE_CODING_PLAN_MODEL_IDS: tuple[str, ...] = (
    "ark-code-latest",
    "doubao-seed-2.0-code",
    "doubao-seed-code",
    "glm-4.7",
    "deepseek-v3.2",
    "kimi-k2.5",
)


def coding_plan_model_infos() -> frozenset[ProviderModelInfo]:
    return model_infos_from_ids(VOLCENGINE_CODING_PLAN_MODEL_IDS)
