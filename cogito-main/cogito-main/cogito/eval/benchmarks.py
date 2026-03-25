"""Benchmark suite for comparing models on the Cogito Score."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from cogito.config.settings import CogitoSettings
from cogito.eval.runner import EvaluationRunner, EvaluationResult

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkEntry:
    model_id: str
    result: Optional[EvaluationResult] = None


class BenchmarkSuite:
    """Run evaluations across multiple models and compare."""

    def __init__(self, settings: CogitoSettings) -> None:
        self.settings = settings
        self.runner = EvaluationRunner(settings)
        self.entries: list[BenchmarkEntry] = []

    def add_model(self, model_id: str) -> None:
        self.entries.append(BenchmarkEntry(model_id=model_id))

    async def run_all(self) -> list[BenchmarkEntry]:
        """Evaluate all registered models."""
        for entry in self.entries:
            logger.info("benchmarking %s", entry.model_id)
            entry.result = await self.runner.run(model_id=entry.model_id)
        return self.entries

    def leaderboard(self) -> list[dict[str, Any]]:
        """Return sorted leaderboard."""
        board = []
        for entry in self.entries:
            if entry.result:
                board.append({
                    "model": entry.model_id,
                    "cogito_score": round(entry.result.cogito_score, 2),
                    "dimensions": entry.result.dimension_scores,
                })
        return sorted(board, key=lambda x: x["cogito_score"], reverse=True)

    def save_leaderboard(self, output_dir: str = "reports") -> Path:
        """Save leaderboard to JSON."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        path = out / "leaderboard.json"
        path.write_text(json.dumps(self.leaderboard(), indent=2))
        logger.info("leaderboard saved to %s", path)
        return path
