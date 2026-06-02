"""Static model catalogs for Kimi Code (Coding Plan)."""

from __future__ import annotations

from providers.model_listing import ProviderModelInfo, model_infos_from_ids

KIMI_CODING_PLAN_MODEL_IDS: tuple[str, ...] = (
    "kimi-for-coding",
    "kimi-k2.6",
    "kimi-k2.5",
)


def coding_plan_model_infos() -> frozenset[ProviderModelInfo]:
    return model_infos_from_ids(KIMI_CODING_PLAN_MODEL_IDS)
