"""Neutral provider catalog: IDs, credentials, defaults, proxy and capability metadata.

Adapter factories live in :mod:`providers.registry`; this module stays free of
provider implementation imports (see contract tests).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

TransportType = Literal["openai_chat", "anthropic_messages"]

# Default upstream base URLs (also re-exported via :mod:`providers.defaults`)
NVIDIA_NIM_DEFAULT_BASE = "https://integrate.api.nvidia.com/v1"
KIMI_DEFAULT_BASE = "https://api.moonshot.ai/v1"
WAFER_DEFAULT_BASE = "https://pass.wafer.ai/v1"
# DeepSeek Anthropic-compatible Messages API (not OpenAI ``/v1`` chat completions).
DEEPSEEK_ANTHROPIC_DEFAULT_BASE = "https://api.deepseek.com/anthropic"
# Historical export name: DeepSeek upstream is the native Anthropic path above.
DEEPSEEK_DEFAULT_BASE = DEEPSEEK_ANTHROPIC_DEFAULT_BASE
FIREWORKS_DEFAULT_BASE = "https://api.fireworks.ai/inference/v1"
OPENROUTER_DEFAULT_BASE = "https://openrouter.ai/api/v1"
LMSTUDIO_DEFAULT_BASE = "http://localhost:1234/v1"
LLAMACPP_DEFAULT_BASE = "http://localhost:8080/v1"
OLLAMA_DEFAULT_BASE = "http://localhost:11434"
OPENCODE_DEFAULT_BASE = "https://opencode.ai/zen/v1"
OPENCODE_GO_DEFAULT_BASE = "https://opencode.ai/zen/go/v1"
ZAI_DEFAULT_BASE = "https://api.z.ai/api/coding/paas/v4"
BAILIAN_CODING_PLAN_DEFAULT_BASE = (
    "https://coding.dashscope.aliyuncs.com/apps/anthropic/v1"
)
BAILIAN_TOKEN_PLAN_DEFAULT_BASE = (
    "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1"
)
VOLCENGINE_CODING_PLAN_DEFAULT_BASE = "https://ark.cn-beijing.volces.com/api/coding/v1"
ZHIPU_CODING_PLAN_DEFAULT_BASE = "https://open.bigmodel.cn/api/anthropic/v1"
KIMI_CODING_PLAN_DEFAULT_BASE = "https://api.kimi.com/coding/v1"
MINIMAX_TOKEN_PLAN_DEFAULT_BASE = "https://api.minimax.io/anthropic/v1"


@dataclass(frozen=True, slots=True)
class ProviderDescriptor:
    """Metadata for building :class:`~providers.base.ProviderConfig` and factory wiring."""

    provider_id: str
    transport_type: TransportType
    capabilities: tuple[str, ...]
    credential_env: str | None = None
    credential_url: str | None = None
    credential_attr: str | None = None
    static_credential: str | None = None
    default_base_url: str | None = None
    base_url_attr: str | None = None
    proxy_attr: str | None = None


PROVIDER_CATALOG: dict[str, ProviderDescriptor] = {
    "nvidia_nim": ProviderDescriptor(
        provider_id="nvidia_nim",
        transport_type="openai_chat",
        credential_env="NVIDIA_NIM_API_KEY",
        credential_url="https://build.nvidia.com/settings/api-keys",
        credential_attr="nvidia_nim_api_key",
        default_base_url=NVIDIA_NIM_DEFAULT_BASE,
        proxy_attr="nvidia_nim_proxy",
        capabilities=("chat", "streaming", "tools", "thinking", "rate_limit"),
    ),
    "open_router": ProviderDescriptor(
        provider_id="open_router",
        transport_type="anthropic_messages",
        credential_env="OPENROUTER_API_KEY",
        credential_url="https://openrouter.ai/keys",
        credential_attr="open_router_api_key",
        default_base_url=OPENROUTER_DEFAULT_BASE,
        proxy_attr="open_router_proxy",
        capabilities=("chat", "streaming", "tools", "thinking", "native_anthropic"),
    ),
    "deepseek": ProviderDescriptor(
        provider_id="deepseek",
        transport_type="anthropic_messages",
        credential_env="DEEPSEEK_API_KEY",
        credential_url="https://platform.deepseek.com/api_keys",
        credential_attr="deepseek_api_key",
        default_base_url=DEEPSEEK_ANTHROPIC_DEFAULT_BASE,
        capabilities=("chat", "streaming", "tools", "thinking", "native_anthropic"),
    ),
    "lmstudio": ProviderDescriptor(
        provider_id="lmstudio",
        transport_type="anthropic_messages",
        static_credential="lm-studio",
        default_base_url=LMSTUDIO_DEFAULT_BASE,
        base_url_attr="lm_studio_base_url",
        proxy_attr="lmstudio_proxy",
        capabilities=("chat", "streaming", "tools", "native_anthropic", "local"),
    ),
    "llamacpp": ProviderDescriptor(
        provider_id="llamacpp",
        transport_type="anthropic_messages",
        static_credential="llamacpp",
        default_base_url=LLAMACPP_DEFAULT_BASE,
        base_url_attr="llamacpp_base_url",
        proxy_attr="llamacpp_proxy",
        capabilities=("chat", "streaming", "tools", "native_anthropic", "local"),
    ),
    "ollama": ProviderDescriptor(
        provider_id="ollama",
        transport_type="anthropic_messages",
        static_credential="ollama",
        default_base_url=OLLAMA_DEFAULT_BASE,
        base_url_attr="ollama_base_url",
        capabilities=(
            "chat",
            "streaming",
            "tools",
            "thinking",
            "native_anthropic",
            "local",
        ),
    ),
    "kimi": ProviderDescriptor(
        provider_id="kimi",
        transport_type="openai_chat",
        credential_env="KIMI_API_KEY",
        credential_url="https://platform.moonshot.cn/console/api-keys",
        credential_attr="kimi_api_key",
        default_base_url=KIMI_DEFAULT_BASE,
        proxy_attr="kimi_proxy",
        capabilities=("chat", "streaming", "tools"),
    ),
    "wafer": ProviderDescriptor(
        provider_id="wafer",
        transport_type="anthropic_messages",
        credential_env="WAFER_API_KEY",
        credential_url="https://www.wafer.ai/pass",
        credential_attr="wafer_api_key",
        default_base_url=WAFER_DEFAULT_BASE,
        proxy_attr="wafer_proxy",
        capabilities=("chat", "streaming", "tools", "thinking", "native_anthropic"),
    ),
    "opencode": ProviderDescriptor(
        provider_id="opencode",
        transport_type="openai_chat",
        credential_env="OPENCODE_API_KEY",
        credential_url="https://opencode.ai/auth",
        credential_attr="opencode_api_key",
        default_base_url=OPENCODE_DEFAULT_BASE,
        proxy_attr="opencode_proxy",
        capabilities=("chat", "streaming", "tools", "thinking", "rate_limit"),
    ),
    "opencode_go": ProviderDescriptor(
        provider_id="opencode_go",
        transport_type="openai_chat",
        credential_env="OPENCODE_API_KEY",
        credential_url="https://opencode.ai/auth",
        credential_attr="opencode_api_key",
        default_base_url=OPENCODE_GO_DEFAULT_BASE,
        proxy_attr="opencode_go_proxy",
        capabilities=("chat", "streaming", "tools", "thinking", "rate_limit"),
    ),
    "zai": ProviderDescriptor(
        provider_id="zai",
        transport_type="openai_chat",
        credential_env="ZAI_API_KEY",
        credential_attr="zai_api_key",
        default_base_url=ZAI_DEFAULT_BASE,
        proxy_attr="zai_proxy",
        capabilities=("chat", "streaming", "tools", "thinking", "rate_limit"),
    ),
    "fireworks": ProviderDescriptor(
        provider_id="fireworks",
        transport_type="openai_chat",
        credential_env="FIREWORKS_API_KEY",
        credential_url="https://fireworks.ai/account/api-keys",
        credential_attr="fireworks_api_key",
        default_base_url=FIREWORKS_DEFAULT_BASE,
        proxy_attr="fireworks_proxy",
        capabilities=("chat", "streaming", "tools", "thinking", "rate_limit"),
    ),
    "bailian_coding_plan": ProviderDescriptor(
        provider_id="bailian_coding_plan",
        transport_type="anthropic_messages",
        credential_env="BAILIAN_CODING_PLAN_API_KEY",
        credential_url="https://help.aliyun.com/zh/model-studio/coding-plan",
        credential_attr="bailian_coding_plan_api_key",
        default_base_url=BAILIAN_CODING_PLAN_DEFAULT_BASE,
        base_url_attr="bailian_coding_plan_base_url",
        proxy_attr="bailian_coding_plan_proxy",
        capabilities=(
            "chat",
            "streaming",
            "tools",
            "thinking",
            "native_anthropic",
            "rate_limit",
        ),
    ),
    "bailian_token_plan": ProviderDescriptor(
        provider_id="bailian_token_plan",
        transport_type="anthropic_messages",
        credential_env="BAILIAN_TOKEN_PLAN_API_KEY",
        credential_url="https://help.aliyun.com/zh/model-studio/more-tools",
        credential_attr="bailian_token_plan_api_key",
        default_base_url=BAILIAN_TOKEN_PLAN_DEFAULT_BASE,
        base_url_attr="bailian_token_plan_base_url",
        proxy_attr="bailian_token_plan_proxy",
        capabilities=(
            "chat",
            "streaming",
            "tools",
            "thinking",
            "native_anthropic",
            "rate_limit",
        ),
    ),
    "volcengine_coding_plan": ProviderDescriptor(
        provider_id="volcengine_coding_plan",
        transport_type="anthropic_messages",
        credential_env="VOLCENGINE_CODING_PLAN_API_KEY",
        credential_url="https://console.volcengine.com/ark/region:ark+cn-beijing/apikey",
        credential_attr="volcengine_coding_plan_api_key",
        default_base_url=VOLCENGINE_CODING_PLAN_DEFAULT_BASE,
        base_url_attr="volcengine_coding_plan_base_url",
        proxy_attr="volcengine_coding_plan_proxy",
        capabilities=(
            "chat",
            "streaming",
            "tools",
            "thinking",
            "native_anthropic",
            "rate_limit",
        ),
    ),
    "zhipu_coding_plan": ProviderDescriptor(
        provider_id="zhipu_coding_plan",
        transport_type="anthropic_messages",
        credential_env="ZHIPU_CODING_PLAN_API_KEY",
        credential_url="https://open.bigmodel.cn/usercenter/apikeys",
        credential_attr="zhipu_coding_plan_api_key",
        default_base_url=ZHIPU_CODING_PLAN_DEFAULT_BASE,
        base_url_attr="zhipu_coding_plan_base_url",
        proxy_attr="zhipu_coding_plan_proxy",
        capabilities=(
            "chat",
            "streaming",
            "tools",
            "thinking",
            "native_anthropic",
            "rate_limit",
        ),
    ),
    "kimi_coding_plan": ProviderDescriptor(
        provider_id="kimi_coding_plan",
        transport_type="anthropic_messages",
        credential_env="KIMI_CODING_PLAN_API_KEY",
        credential_url="https://www.kimi.com/code",
        credential_attr="kimi_coding_plan_api_key",
        default_base_url=KIMI_CODING_PLAN_DEFAULT_BASE,
        base_url_attr="kimi_coding_plan_base_url",
        proxy_attr="kimi_coding_plan_proxy",
        capabilities=(
            "chat",
            "streaming",
            "tools",
            "thinking",
            "native_anthropic",
            "rate_limit",
        ),
    ),
    "minimax_token_plan": ProviderDescriptor(
        provider_id="minimax_token_plan",
        transport_type="anthropic_messages",
        credential_env="MINIMAX_TOKEN_PLAN_API_KEY",
        credential_url="https://platform.minimax.io/user-center/basic-information",
        credential_attr="minimax_token_plan_api_key",
        default_base_url=MINIMAX_TOKEN_PLAN_DEFAULT_BASE,
        base_url_attr="minimax_token_plan_base_url",
        proxy_attr="minimax_token_plan_proxy",
        capabilities=(
            "chat",
            "streaming",
            "tools",
            "thinking",
            "native_anthropic",
            "rate_limit",
        ),
    ),
}

# Order matches docs / historical error text; must match PROVIDER_CATALOG keys.
SUPPORTED_PROVIDER_IDS: tuple[str, ...] = tuple(PROVIDER_CATALOG.keys())

if len(set(SUPPORTED_PROVIDER_IDS)) != len(SUPPORTED_PROVIDER_IDS):
    raise AssertionError("Duplicate provider ids in PROVIDER_CATALOG key order")
