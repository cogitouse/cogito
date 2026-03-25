"""Local model provider (Ollama, vLLM, LM Studio)."""

from __future__ import annotations

import httpx

from cogito.providers.base import ModelProvider


class LocalProvider(ModelProvider):
    """Connects to a local OpenAI-compatible API (Ollama, vLLM, LM Studio)."""

    def __init__(
        self,
        model: str = "llama3",
        base_url: str = "http://localhost:11434/v1",
    ) -> None:
        self.model = model
        self._client = httpx.AsyncClient(base_url=base_url, timeout=120.0)

    async def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> str:
        resp = await self._client.post(
            "/chat/completions",
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    async def embed(self, text: str) -> list[float]:
        resp = await self._client.post(
            "/embeddings",
            json={"model": self.model, "input": text},
        )
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]
