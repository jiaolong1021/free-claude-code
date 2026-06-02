"""Tests for shared Anthropic subscription plan transport utilities."""

from __future__ import annotations

import pytest

from providers.bailian import (
    BAILIAN_CODING_PLAN_BASE_URL,
    BAILIAN_CODING_PLAN_INTL_BASE_URL,
    normalize_bailian_anthropic_base_url,
)
from providers.kimi import normalize_kimi_coding_plan_base_url
from providers.minimax import (
    MINIMAX_TOKEN_PLAN_BASE_URL,
    normalize_minimax_token_plan_base_url,
)
from providers.plan import append_v1_suffix, normalize_with_suffix_map
from providers.volcengine import (
    VOLCENGINE_CODING_PLAN_BASE_URL,
    normalize_volcengine_coding_plan_base_url,
)
from providers.zhipu import (
    ZHIPU_CODING_PLAN_BASE_URL,
    normalize_zhipu_coding_plan_base_url,
)


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


@pytest.mark.parametrize(
    ("normalize", "configured", "default", "expected"),
    [
        (
            normalize_bailian_anthropic_base_url,
            "https://coding.dashscope.aliyuncs.com/v1",
            BAILIAN_CODING_PLAN_BASE_URL,
            BAILIAN_CODING_PLAN_BASE_URL,
        ),
        (
            normalize_bailian_anthropic_base_url,
            "https://coding-intl.dashscope.aliyuncs.com/v1",
            BAILIAN_CODING_PLAN_BASE_URL,
            BAILIAN_CODING_PLAN_INTL_BASE_URL,
        ),
        (
            normalize_volcengine_coding_plan_base_url,
            "https://ark.cn-beijing.volces.com/api/coding",
            VOLCENGINE_CODING_PLAN_BASE_URL,
            VOLCENGINE_CODING_PLAN_BASE_URL,
        ),
        (
            normalize_zhipu_coding_plan_base_url,
            "https://open.bigmodel.cn/api/coding/paas/v4",
            ZHIPU_CODING_PLAN_BASE_URL,
            ZHIPU_CODING_PLAN_BASE_URL,
        ),
        (
            normalize_zhipu_coding_plan_base_url,
            "https://open.bigmodel.cn/api/anthropic",
            ZHIPU_CODING_PLAN_BASE_URL,
            ZHIPU_CODING_PLAN_BASE_URL,
        ),
        (
            normalize_kimi_coding_plan_base_url,
            "https://api.kimi.com/coding",
            "https://api.kimi.com/coding/v1",
            "https://api.kimi.com/coding/v1",
        ),
        (
            normalize_minimax_token_plan_base_url,
            "https://api.minimax.io/anthropic",
            MINIMAX_TOKEN_PLAN_BASE_URL,
            MINIMAX_TOKEN_PLAN_BASE_URL,
        ),
    ],
)
def test_plan_base_url_normalizers(normalize, configured, default, expected):
    assert normalize(configured, default) == expected
