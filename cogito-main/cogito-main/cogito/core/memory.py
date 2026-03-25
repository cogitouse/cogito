"""Sliding-window memory store with episodic and semantic layers."""

from __future__ import annotations

import logging
from collections import deque
from typing import Any

logger = logging.getLogger(__name__)


class MemoryStore:
    """Token-bounded sliding window memory."""

    def __init__(self, capacity: int = 200_000) -> None:
        self.capacity = capacity
        self._episodes: deque[dict[str, Any]] = deque()
        self._semantic: dict[str, Any] = {}
        self._token_count = 0

    def store(self, **kwargs: Any) -> None:
        """Store an episode and evict oldest if over capacity."""
        episode = dict(kwargs)
        est_tokens = self._estimate_tokens(episode)
        self._episodes.append(episode)
        self._token_count += est_tokens

        while self._token_count > self.capacity and self._episodes:
            evicted = self._episodes.popleft()
            self._token_count -= self._estimate_tokens(evicted)
            self._extract_semantic(evicted)

        logger.debug(
            "memory: %d episodes, ~%d tokens", len(self._episodes), self._token_count
        )

    def context(self) -> list[dict[str, Any]]:
        """Return recent episodes as context for reasoning."""
        return list(self._episodes)

    def usage(self) -> dict[str, int]:
        """Return memory usage statistics."""
        return {
            "episodes": len(self._episodes),
            "token_count": self._token_count,
            "capacity": self.capacity,
            "semantic_keys": len(self._semantic),
        }

    def _estimate_tokens(self, data: dict[str, Any]) -> int:
        """Rough token estimate from string representation."""
        return len(str(data)) // 4

    def _extract_semantic(self, episode: dict[str, Any]) -> None:
        """Extract durable facts from an evicted episode into semantic memory."""
        cycle = episode.get("cycle", 0)
        if results := episode.get("results"):
            self._semantic[f"cycle_{cycle}"] = {
                "summary": f"Cycle {cycle} completed with {len(results)} actions",
                "timestamp": episode.get("timestamp"),
            }
