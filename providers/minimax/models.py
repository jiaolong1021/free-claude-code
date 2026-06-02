"""Static model catalogs for MiniMax Token Plan."""

from __future__ import annotations

from providers.model_listing import ProviderModelInfo, model_infos_from_ids

MINIMAX_TOKEN_PLAN_MODEL_IDS: tuple[str, ...] = (
    "MiniMax-M3",
    "MiniMax-M2.7",
    "MiniMax-M2.7-highspeed",
    "MiniMax-M2.5",
    "MiniMax-M2.5-highspeed",
    "MiniMax-M2.1",
    "MiniMax-M2.1-highspeed",
    "MiniMax-M2",
)


def token_plan_model_infos() -> frozenset[ProviderModelInfo]:
    return model_infos_from_ids(MINIMAX_TOKEN_PLAN_MODEL_IDS)
