"""Static model catalogs for subscription plan providers."""

from __future__ import annotations

from providers.model_listing import ProviderModelInfo, model_infos_from_ids

BAILIAN_CODING_PLAN_MODEL_IDS: tuple[str, ...] = (
    "qwen3.6-plus",
    "kimi-k2.5",
    "glm-5",
    "MiniMax-M2.5",
    "qwen3.5-plus",
    "qwen3-max-2026-01-23",
    "qwen3-coder-next",
    "qwen3-coder-plus",
    "glm-4.7",
)

BAILIAN_TOKEN_PLAN_MODEL_IDS: tuple[str, ...] = (
    "qwen3-coder-plus",
    "qwen3.5-plus",
    "qwen3.6-plus",
    "qwen3-coder-next",
)

VOLCENGINE_CODING_PLAN_MODEL_IDS: tuple[str, ...] = (
    "ark-code-latest",
    "doubao-seed-2.0-code",
    "doubao-seed-code",
    "glm-4.7",
    "deepseek-v3.2",
    "kimi-k2.5",
)

ZHIPU_CODING_PLAN_MODEL_IDS: tuple[str, ...] = (
    "glm-5.1",
    "glm-5-turbo",
    "glm-4.7",
    "glm-4.5-air",
)

KIMI_CODING_PLAN_MODEL_IDS: tuple[str, ...] = (
    "kimi-for-coding",
    "kimi-k2.6",
    "kimi-k2.5",
)

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


def model_infos_for_ids(model_ids: tuple[str, ...]) -> frozenset[ProviderModelInfo]:
    return model_infos_from_ids(model_ids)
