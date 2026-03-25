"""Anthropic Claude model provider."""

from __future__ import annotations

import httpx

from cogito.providers.base import ModelProvider


class AnthropicProvider(ModelProvider):
    BASE_URL = "https://api.anthropic.com/v1"

    def __init__(self, api_key: str | None, model: str = "claude-3-opus-20240229") -> None:
        self.api_key = api_key
        self.model = model
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "x-api-key": api_key or "",
                "anthropic-version": "2023-06-01",
            },
            timeout=60.0,
        )

    async def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> str:
        # separate system message
        system = ""
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                user_messages.append(msg)

        body: dict = {
            "model": self.model,
            "messages": user_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system:
            body["system"] = system

        resp = await self._client.post("/messages", json=body)
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]

    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Anthropic does not provide embeddings")
