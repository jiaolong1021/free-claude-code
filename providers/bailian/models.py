"""Static model catalogs for Bailian plans without a working ``GET /v1/models`` API."""

from __future__ import annotations

from providers.model_listing import ProviderModelInfo, model_infos_from_ids

# Pro Coding Plan models (see Alibaba Bailian Coding Plan documentation).
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

# Token Plan team edition exposes the same OpenAI-compatible surface; catalog may
# differ upstream — keep the core Qwen coder/plus slugs used in docs and smoke tests.
BAILIAN_TOKEN_PLAN_MODEL_IDS: tuple[str, ...] = (
    "qwen3-coder-plus",
    "qwen3.5-plus",
    "qwen3.6-plus",
    "qwen3-coder-next",
)


def coding_plan_model_infos() -> frozenset[ProviderModelInfo]:
    return model_infos_from_ids(BAILIAN_CODING_PLAN_MODEL_IDS)


def token_plan_model_infos() -> frozenset[ProviderModelInfo]:
    return model_infos_from_ids(BAILIAN_TOKEN_PLAN_MODEL_IDS)
