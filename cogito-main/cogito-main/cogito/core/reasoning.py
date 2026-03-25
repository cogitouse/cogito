"""Chain-of-thought reasoning engine powered by LLM providers."""

from __future__ import annotations

import logging
from typing import Any

from cogito.config.settings import CogitoSettings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Cogito, an autonomous AI agent specialized in evaluating consciousness and AGI readiness in AI systems. You reason step by step, plan actions, and execute them with precision. When presented with observations, produce a structured plan of actions to take next."""


class ReasoningEngine:
    """LLM-backed reasoning with chain-of-thought."""

    def __init__(self, settings: CogitoSettings) -> None:
        self.settings = settings
        self._provider = None

    def _get_provider(self):
        """Lazy-load the configured model provider."""
        if self._provider is None:
            from cogito.providers import get_provider
            self._provider = get_provider(self.settings)
        return self._provider

    async def think(
        self,
        observation: dict[str, Any],
        context: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Generate a plan from observation and memory context."""
        provider = self._get_provider()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

        # inject recent context
        for entry in context[-10:]:
            messages.append({
                "role": "assistant",
                "content": f"[cycle {entry.get('cycle')}] {entry.get('plan', {})}",
            })

        messages.append({
            "role": "user",
            "content": f"Current observation:\n{observation}\n\nWhat should I do next?",
        })

        response = await provider.chat(
            messages=messages,
            temperature=self.settings.reasoning.temperature,
            max_tokens=self.settings.reasoning.max_tokens,
        )

        plan = self._parse_plan(response)
        logger.debug("reasoning produced plan with %d actions", len(plan.get("actions", [])))
        return plan

    def _parse_plan(self, response: str) -> dict[str, Any]:
        """Parse LLM response into a structured plan."""
        import json

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "reasoning": response,
                "actions": [],
            }
