"""Static model catalogs for Zhipu GLM Coding Plan."""

from __future__ import annotations

from providers.model_listing import ProviderModelInfo, model_infos_from_ids

ZHIPU_CODING_PLAN_MODEL_IDS: tuple[str, ...] = (
    "glm-5.1",
    "glm-5-turbo",
    "glm-4.7",
    "glm-4.5-air",
)


def coding_plan_model_infos() -> frozenset[ProviderModelInfo]:
    return model_infos_from_ids(ZHIPU_CODING_PLAN_MODEL_IDS)
