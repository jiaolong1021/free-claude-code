"""User-defined Anthropic-compatible endpoint (custom base URL and API key)."""

from __future__ import annotations

from typing import Literal

from providers.anthropic_messages import AnthropicMessagesTransport
from providers.base import ProviderConfig
from providers.model_listing import ProviderModelInfo, model_infos_from_ids

_ANTHROPIC_VERSION = "2023-06-01"
CustomAnthropicAuthStyle = Literal["x_api_key", "bearer"]


class CustomAnthropicProvider(AnthropicMessagesTransport):
    """Anthropic Messages transport for a user-supplied upstream root URL."""

    def __init__(
        self,
        config: ProviderConfig,
        *,
        model_ids: frozenset[str],
        auth_style: CustomAnthropicAuthStyle = "x_api_key",
    ):
        self._catalog_model_ids = model_ids
        self._auth_style = auth_style
        normalized = (config.base_url or "").rstrip("/")
        effective_config = config.model_copy(update={"base_url": normalized})
        super().__init__(
            effective_config,
            provider_name="CUSTOM_ANTHROPIC",
            default_base_url=normalized,
        )

    async def list_model_infos(self) -> frozenset[ProviderModelInfo]:
        if self._catalog_model_ids:
            return model_infos_from_ids(self._catalog_model_ids)
        return await super().list_model_infos()

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
