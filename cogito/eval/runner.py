"""Evaluation pipeline orchestrator."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

from cogito.config.settings import CogitoSettings
from cogito.eval.dimensions import DIMENSIONS, CognitiveDimension
from cogito.eval.scoring import compute_cogito_score

logger = logging.getLogger(__name__)


class EvaluationResult:
    """Container for evaluation results."""

    def __init__(
        self,
        model_id: str,
        dimension_scores: dict[str, float],
        cogito_score: float,
        raw_responses: dict[str, list[dict[str, Any]]],
    ) -> None:
        self.model_id = model_id
        self.dimension_scores = dimension_scores
        self.cogito_score = cogito_score
        self.raw_responses = raw_responses

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "cogito_score": round(self.cogito_score, 2),
            "dimension_scores": {
                k: round(v, 2) for k, v in self.dimension_scores.items()
            },
        }


class EvaluationRunner:
    """Orchestrates evaluation across cognitive dimensions."""

    def __init__(self, settings: CogitoSettings) -> None:
        self.settings = settings

    async def run(
        self,
        model_id: str,
        dimensions: Optional[list[str]] = None,
    ) -> EvaluationResult:
        """Run evaluation on a model across specified dimensions."""
        from cogito.providers import get_provider

        provider = get_provider(self.settings)
        target_dims = self._resolve_dimensions(dimensions)

        logger.info("evaluating %s across %d dimensions", model_id, len(target_dims))

        dimension_scores: dict[str, float] = {}
        raw_responses: dict[str, list[dict[str, Any]]] = {}

        for dim in target_dims:
            score, responses = await self._evaluate_dimension(provider, dim)
            dimension_scores[dim.name] = score
            raw_responses[dim.name] = responses
            logger.info("  %s: %.2f", dim.name, score)

        cogito_score = compute_cogito_score(dimension_scores)
        logger.info("Cogito Score for %s: %.2f", model_id, cogito_score)

        return EvaluationResult(
            model_id=model_id,
            dimension_scores=dimension_scores,
            cogito_score=cogito_score,
            raw_responses=raw_responses,
        )

    async def _evaluate_dimension(
        self, provider: Any, dim: CognitiveDimension
    ) -> tuple[float, list[dict[str, Any]]]:
        """Evaluate a single cognitive dimension."""
        responses: list[dict[str, Any]] = []
        total_score = 0.0
        n_probes = min(
            self.settings.evaluation.probes_per_dimension, len(dim.probes)
        )

        for probe in dim.probes[:n_probes]:
            result = await provider.chat(
                messages=[
                    {"role": "system", "content": dim.system_prompt},
                    {"role": "user", "content": probe["prompt"]},
                ],
                temperature=0.1,
                max_tokens=2048,
            )
            score = dim.score_fn(result, probe)
            total_score += score
            responses.append({
                "probe": probe["id"],
                "response": result,
                "score": score,
            })

        avg = total_score / max(n_probes, 1)
        return avg * 100.0, responses

    def _resolve_dimensions(
        self, names: Optional[list[str]]
    ) -> list[CognitiveDimension]:
        """Resolve dimension names to CognitiveDimension objects."""
        if names is None:
            return list(DIMENSIONS.values())
        resolved = []
        for name in names:
            if name in DIMENSIONS:
                resolved.append(DIMENSIONS[name])
            else:
                logger.warning("unknown dimension: %s", name)
        return resolved

    def save_report(self, result: EvaluationResult, output_dir: str = "reports") -> Path:
        """Save evaluation report to disk."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"{result.model_id.replace('/', '_')}_report.json"
        path.write_text(json.dumps(result.to_dict(), indent=2))
        logger.info("report saved to %s", path)
        return path
