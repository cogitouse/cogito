"""xAI Grok model provider."""

from __future__ import annotations

import httpx

from cogito.providers.base import ModelProvider


class GrokProvider(ModelProvider):
    BASE_URL = "https://api.x.ai/v1"

    def __init__(self, api_key: str | None, model: str = "grok-3") -> None:
        self.api_key = api_key
        self.model = model
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0,
        )

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
            json={"model": "grok-embed", "input": text},
        )
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]
