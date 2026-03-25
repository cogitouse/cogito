"""Abstract base class for model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ModelProvider(ABC):
    """Interface that all model providers must implement."""

    @abstractmethod
    async def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> str:
        """Send a chat completion request and return the response text."""
        ...

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for the given text."""
        ...
