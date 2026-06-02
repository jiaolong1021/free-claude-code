"""Freeze ``PROVIDER_CATALOG`` insertion order used as canonical provider ranking."""

from __future__ import annotations

from config.provider_catalog import PROVIDER_CATALOG, SUPPORTED_PROVIDER_IDS

_EXPECTED_PROVIDER_ORDER: tuple[str, ...] = (
    "nvidia_nim",
    "open_router",
    "gemini",
    "deepseek",
    "mistral",
    "mistral_codestral",
    "opencode",
    "opencode_go",
    "wafer",
    "kimi",
    "cerebras",
    "groq",
    "fireworks",
    "zai",
    "lmstudio",
    "llamacpp",
    "ollama",
    "bailian_coding_plan",
    "bailian_token_plan",
    "volcengine_coding_plan",
    "zhipu_coding_plan",
    "kimi_coding_plan",
    "minimax_token_plan",
)


def test_provider_catalog_key_order_matches_canonical_plan() -> None:
    """NIM first; DeepSeek fourth; Wafer ninth / Kimi tenth (see contributor plan)."""

    assert tuple(PROVIDER_CATALOG.keys()) == _EXPECTED_PROVIDER_ORDER
    assert SUPPORTED_PROVIDER_IDS == _EXPECTED_PROVIDER_ORDER
