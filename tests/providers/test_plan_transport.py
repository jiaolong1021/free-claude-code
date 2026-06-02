"""Tests for shared Anthropic subscription plan transport utilities."""

from providers.plan import append_v1_suffix, normalize_with_suffix_map


def test_append_v1_suffix_idempotent():
    assert (
        append_v1_suffix("https://example.com/api/anthropic/v1")
        == "https://example.com/api/anthropic/v1"
    )


def test_append_v1_suffix_from_anthropic_root():
    assert (
        append_v1_suffix("https://example.com/api/anthropic")
        == "https://example.com/api/anthropic/v1"
    )


def test_append_v1_suffix_from_coding_root():
    assert (
        append_v1_suffix("https://ark.cn-beijing.volces.com/api/coding")
        == "https://ark.cn-beijing.volces.com/api/coding/v1"
    )


def test_normalize_with_suffix_map_applies_legacy_mapping():
    mapped = normalize_with_suffix_map(
        "https://legacy.example/v1",
        "https://default.example/v1",
        legacy_map={"https://legacy.example/v1": "https://mapped.example/v1"},
    )
    assert mapped == "https://mapped.example/v1"
