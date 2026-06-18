"""Factory helpers for Anthropic-compatible subscription plan providers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from providers.base import ProviderConfig
from providers.model_listing import ProviderModelInfo

from .normalize import normalize_with_suffix_map
from .transport import AnthropicSubscriptionPlanTransport, PlanAuthStyle


class PlanProvider(Protocol):
    """Provider adapter constructed from a single :class:`ProviderConfig`."""

    def __init__(self, config: ProviderConfig) -> None: ...


def base_url_normalizer(
    *,
    default: str,
    legacy_map: dict[str, str],
    suffix_rewrites: tuple[tuple[str, str], ...] = (),
) -> Callable[[str, str], str]:
    """Return a ``(configured, fallback) -> normalized`` helper for tests and docs."""

    def normalize(configured: str, fallback: str = default) -> str:
        return normalize_with_suffix_map(
            configured,
            fallback,
            legacy_map=legacy_map,
            suffix_rewrites=suffix_rewrites,
        )

    return normalize


def plan_provider(
    *,
    class_name: str,
    provider_name: str,
    default_base_url: str,
    model_ids: tuple[str, ...],
    legacy_base_map: dict[str, str] | None = None,
    suffix_rewrites: tuple[tuple[str, str], ...] = (),
    auth_style: PlanAuthStyle = "x_api_key",
    catalog: Callable[[], frozenset[ProviderModelInfo]] | None = None,
) -> type[PlanProvider]:
    """Build a plan provider class with shared transport behavior."""
    if catalog is not None:
        resolved_catalog = catalog
    else:
        from .catalogs import model_infos_for_ids

        cached = model_infos_for_ids(model_ids)

        def resolved_catalog() -> frozenset[ProviderModelInfo]:
            return cached

    legacy_map = legacy_base_map or {}

    class _PlanProvider(AnthropicSubscriptionPlanTransport):
        def __init__(self, config: ProviderConfig):
            super().__init__(
                config,
                provider_name=provider_name,
                default_base_url=default_base_url,
                catalog=resolved_catalog,
                legacy_base_map=legacy_map,
                suffix_rewrites=suffix_rewrites,
                auth_style=auth_style,
            )

    _PlanProvider.__name__ = class_name
    _PlanProvider.__qualname__ = class_name
    plan_provider_cls: type[PlanProvider] = _PlanProvider
    return plan_provider_cls
