"""Base URL normalization for Anthropic-compatible subscription plan endpoints."""

from __future__ import annotations


def append_v1_suffix(base: str) -> str:
    """Ensure the Anthropic Messages root ends with ``/v1``."""
    trimmed = base.rstrip("/")
    if trimmed.endswith("/v1"):
        return trimmed
    if trimmed.endswith("/apps/anthropic"):
        return f"{trimmed}/v1"
    return f"{trimmed}/v1"


def normalize_with_suffix_map(
    configured: str,
    default: str,
    *,
    legacy_map: dict[str, str],
) -> str:
    """Map legacy OpenAI-style bases and append ``/v1`` when needed."""
    base = (configured or default).rstrip("/")
    mapped = legacy_map.get(base)
    if mapped is not None:
        return mapped
    return append_v1_suffix(base)
