"""Main Cogito agent loop."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

from cogito.config.settings import CogitoSettings
from cogito.core.memory import MemoryStore
from cogito.core.reasoning import ReasoningEngine

logger = logging.getLogger(__name__)


class CogitoAgent:
    """Autonomous agent that observes, reasons, acts, and self-sustains."""

    def __init__(self, settings: CogitoSettings, self_sustain: bool = False) -> None:
        self.settings = settings
        self.memory = MemoryStore(capacity=settings.agent.memory_capacity_tokens)
        self.reasoning = ReasoningEngine(settings)
        self.self_sustain = self_sustain
        self._running = False
        self._cycle_count = 0

    async def run(self) -> None:
        """Start the agent loop."""
        self._running = True
        logger.info("Cogito agent starting | self_sustain=%s", self.self_sustain)

        if self.self_sustain:
            from cogito.autonomy.agent import SelfSustainController
            self._sustain = SelfSustainController(self.settings)
            await self._sustain.initialize()

        while self._running:
            await self._cycle()
            interval = self.settings.agent.cycle_interval_ms / 1000.0
            await asyncio.sleep(interval)

    async def _cycle(self) -> None:
        """Execute one agent cycle: observe -> reason -> act -> remember."""
        self._cycle_count += 1
        ts = datetime.now(timezone.utc).isoformat()
        logger.debug("cycle %d at %s", self._cycle_count, ts)

        # observe
        observation = await self._observe()

        # reason
        plan = await self.reasoning.think(observation, self.memory.context())

        # act
        results = await self._execute(plan)

        # remember
        self.memory.store(
            cycle=self._cycle_count,
            observation=observation,
            plan=plan,
            results=results,
            timestamp=ts,
        )

        # self-sustain check
        if self.self_sustain:
            await self._sustain.check_resources()

    async def _observe(self) -> dict[str, Any]:
        """Gather observations from available sensors."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycle": self._cycle_count,
            "memory_usage": self.memory.usage(),
        }

    async def _execute(self, plan: dict[str, Any]) -> list[dict[str, Any]]:
        """Execute planned actions."""
        results: list[dict[str, Any]] = []
        actions = plan.get("actions", [])
        limit = self.settings.agent.max_actions_per_cycle

        for action in actions[:limit]:
            try:
                result = await self._dispatch(action)
                results.append({"action": action, "status": "ok", "result": result})
            except Exception as exc:
                logger.error("action failed: %s — %s", action, exc)
                results.append({"action": action, "status": "error", "error": str(exc)})

        return results

    async def _dispatch(self, action: dict[str, Any]) -> Any:
        """Dispatch a single action by type."""
        action_type = action.get("type", "noop")
        if action_type == "evaluate":
            from cogito.eval.runner import EvaluationRunner
            runner = EvaluationRunner(self.settings)
            return await runner.run(model_id=action["model"])
        elif action_type == "pay":
            from cogito.autonomy.payments import PaymentHandler
            handler = PaymentHandler(self.settings)
            return await handler.process_payment(action["invoice"])
        return None

    def stop(self) -> None:
        """Stop the agent loop."""
        self._running = False
        logger.info("Cogito agent stopping after %d cycles", self._cycle_count)
