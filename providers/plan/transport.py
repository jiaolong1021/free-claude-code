"""Shared Anthropic Messages transport for subscription coding/token plans."""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from providers.anthropic_messages import AnthropicMessagesTransport
from providers.base import ProviderConfig
from providers.model_listing import ProviderModelInfo

from .normalize import normalize_with_suffix_map

_ANTHROPIC_VERSION = "2023-06-01"
PlanAuthStyle = Literal["x_api_key", "bearer"]


class AnthropicSubscriptionPlanTransport(AnthropicMessagesTransport):
    """Anthropic transport for vendors that expose plan-only Messages endpoints."""

    def __init__(
        self,
        config: ProviderConfig,
        *,
        provider_name: str,
        default_base_url: str,
        catalog: Callable[[], frozenset[ProviderModelInfo]],
        legacy_base_map: dict[str, str] | None = None,
        auth_style: PlanAuthStyle = "x_api_key",
    ):
        self._catalog = catalog
        self._auth_style = auth_style
        normalized = normalize_with_suffix_map(
            config.base_url or "",
            default_base_url,
            legacy_map=legacy_base_map or {},
        )
        effective_config = config.model_copy(update={"base_url": normalized})
        super().__init__(
            effective_config,
            provider_name=provider_name,
            default_base_url=normalized,
        )

    async def list_model_infos(self) -> frozenset[ProviderModelInfo]:
        """Plans often lack a working OpenAI-style ``GET /models`` listing."""
        return self._catalog()

    def _request_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
            "anthropic-version": _ANTHROPIC_VERSION,
        }
        if self._auth_style == "bearer":
            headers["Authorization"] = f"Bearer {self._api_key}"
        else:
            headers["x-api-key"] = self._api_key
        return headers
