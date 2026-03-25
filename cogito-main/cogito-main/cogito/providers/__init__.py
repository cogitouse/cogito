"""Model provider module."""

from __future__ import annotations

from cogito.config.settings import CogitoSettings
from cogito.providers.base import ModelProvider


def get_provider(settings: CogitoSettings) -> ModelProvider:
    """Return the appropriate model provider based on config."""
    model = settings.reasoning.model.lower()

    if "gpt" in model or "o1" in model:
        from cogito.providers.openai import OpenAIProvider
        return OpenAIProvider(api_key=settings.openai_api_key, model=settings.reasoning.model)
    elif "claude" in model:
        from cogito.providers.anthropic import AnthropicProvider
        return AnthropicProvider(api_key=settings.anthropic_api_key, model=settings.reasoning.model)
    elif "grok" in model:
        from cogito.providers.grok import GrokProvider
        return GrokProvider(api_key=settings.xai_grok_api_key, model=settings.reasoning.model)
    else:
        from cogito.providers.local import LocalProvider
        return LocalProvider(model=settings.reasoning.model)
